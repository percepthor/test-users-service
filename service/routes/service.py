import ctypes

from cerver.http import HTTP_STATUS_OK
from cerver.http import http_response_json_msg_send
from cerver.http import http_response_json_key_value_send

import config
import runtime
import version

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

# GET *
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def service_catch_all_handler (http_receive, request):
	http_response_json_msg_send (
		http_receive,
		HTTP_STATUS_OK,
		b"Users Service!"
	)
