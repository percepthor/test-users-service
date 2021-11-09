import ctypes

from cerver.http import HTTP_STATUS_OK
from cerver.http import http_request_get_body
from cerver.http import http_response_render_json

import percepthor
from errors import *
import runtime

from controllers.auth import percepthor_user_login, percepthor_user_register

# POST /api/users/login
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def login_handler (http_receive, request):
	error, errors, token = percepthor_user_login (
		http_receive, http_request_get_body (request)
	)

	if (error == SERVICE_ERROR_NONE):
		http_response_render_json (
			http_receive, HTTP_STATUS_OK,
			token, len (token.value)
		)

	elif (errors):
		service_errors_send (error, http_receive, errors)
		
	else:
		service_error_send (error, http_receive)

# POST /api/users/register
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def register_handler (http_receive, request):
	error, errors, token = percepthor_user_register (
		http_receive, http_request_get_body (request)
	)

	if (error == SERVICE_ERROR_NONE):
		http_response_render_json (
			http_receive, HTTP_STATUS_OK,
			token, len (token.value)
		)

	elif (errors):
		service_errors_send (error, http_receive, errors)

	else:
		service_error_send (error, http_receive)
