import ctypes

from cerver.http import HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST
from cerver.http import http_request_get_decoded_data
from cerver.http import http_response_json_msg_send
from cerver.http import http_response_json_key_value_send
from cerver.http import http_response_json_error_send

import percepthor
from errors import SERVICE_ERROR_NOT_FOUND, service_error_send
import runtime
import version

from controllers.users import percepthor_user_load_from_decoded_data

# GET /api/users
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def main_handler (http_receive, request):
	http_response_json_msg_send (
		http_receive,
		HTTP_STATUS_OK,
		b"Users Service Works!"
	)

# GET /api/users/version
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def version_handler (http_receive, request):
	v = f"{version.USERS_VERSION_NAME} - {version.USERS_VERSION_DATE}"

	http_response_json_key_value_send (
		http_receive,
		HTTP_STATUS_OK,
		b"version", v.encode ("utf-8")
	)

# GET /api/users/auth
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def auth_handler (http_receive, request):
	user = percepthor_user_load_from_decoded_data (
		http_request_get_decoded_data (request)
	)

	if (user):
		if (percepthor.RUNTIME == runtime.RUNTIME_TYPE_DEVELOPMENT):
			print (user)

		http_response_json_key_value_send (
			http_receive,
			HTTP_STATUS_OK,
			b"oki", b"doki"
		)

	else:
		http_response_json_error_send (
			http_receive,
			HTTP_STATUS_BAD_REQUEST,
			b"Bad user!"
		)

# GET *
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def service_catch_all_handler (http_receive, request):
	service_error_send (SERVICE_ERROR_NOT_FOUND, http_receive)
