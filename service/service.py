import sys
import ctypes

from cerver import *
from cerver.http import *

from percepthor import *

from routes.auth import *
from routes.service import *

users_service = None

# end
def end (signum, frame):
	# cerver_stats_print (users_service, False, False)
	http_cerver_all_stats_print (http_cerver_get (users_service))
	cerver_teardown (users_service)
	cerver_end ()

	percepthor_end ()

	sys.exit ("Done!")

def service_set_routes (http_cerver):
	# register top level route
	# GET /api/users
	main_route = http_route_create (REQUEST_METHOD_GET, b"api/users", main_handler)
	http_cerver_route_register (http_cerver, main_route)

	# GET /api/users/version
	version_route = http_route_create (REQUEST_METHOD_GET, b"version", version_handler)
	http_route_child_add (main_route, version_route)

	# GET /api/users/auth
	auth_route = http_route_create (REQUEST_METHOD_GET, b"auth", auth_handler)
	http_route_set_auth (auth_route, HTTP_ROUTE_AUTH_TYPE_BEARER)
	http_route_set_decode_data_into_json (auth_route)
	http_route_child_add (main_route, auth_route)

	# auth routes
	# POST api/users/login
	login_route = http_route_create (REQUEST_METHOD_POST, b"login", login_handler)
	http_route_child_add (main_route, login_route)

	# POST api/users/register
	register_route = http_route_create (REQUEST_METHOD_POST, b"register", register_handler)
	http_route_child_add (main_route, register_route)

def start ():
	global users_service
	users_service = cerver_create_web (
		b"users-service", PORT, CERVER_CONNECTION_QUEUE
	)

	# main configuration
	cerver_set_alias (users_service, b"users")

	cerver_set_receive_buffer_size (users_service, CERVER_RECEIVE_BUFFER_SIZE)
	cerver_set_thpool_n_threads (users_service, CERVER_TH_THREADS)
	cerver_set_handler_type (users_service, CERVER_HANDLER_TYPE_THREADS)

	cerver_set_reusable_address_flags (users_service, True)

	# HTTP configuration
	http_cerver = http_cerver_get (users_service)

	http_cerver_auth_set_jwt_algorithm (http_cerver, JWT_ALG_RS256)
	http_cerver_auth_set_jwt_priv_key_filename (http_cerver, PRIV_KEY.encode ("utf-8"))
	http_cerver_auth_set_jwt_pub_key_filename (http_cerver, PUB_KEY.encode ("utf-8"))

	service_set_routes (http_cerver)

	# add a catch all route
	http_cerver_set_catch_all_route (http_cerver, service_catch_all_handler)

	# admin
	http_cerver_enable_admin_routes (http_cerver, True)
	http_cerver_enable_admin_routes_authentication (
		http_cerver, HTTP_ROUTE_AUTH_TYPE_BEARER
	)

	http_cerver_admin_routes_auth_decode_to_json (http_cerver)

	# start
	cerver_start (users_service)
