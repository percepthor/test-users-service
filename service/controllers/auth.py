import ctypes
import json
import time

from cerver.http import http_receive_get_cerver
from cerver.http import http_cerver_auth_jwt_new, http_cerver_auth_jwt_delete
from cerver.http import http_cerver_auth_jwt_add_value, http_cerver_auth_jwt_add_value_int
from cerver.http import http_cerver_auth_generate_bearer_jwt_json
from cerver.http import http_jwt_get_json, http_jwt_get_json_len
from cerver.http import validate_body_value_exists, validate_body_value

from cerver.utils import cerver_log_success, cerver_log_warning, cerver_log_error

import percepthor
from errors import *
import runtime
from validation import *

from models.user import *

from controllers.roles import percepthor_role_get_name_by_oid
from controllers.users import percepthor_user_set_role
from controllers.users import percepthor_user_check_by_email, percepthor_user_get_for_login

HTTP_JWT_TOKEN_SIZE = 4096

def percepthor_user_generate_token (http_receive, user):
	error = SERVICE_ERROR_NONE
	result = None

	http_jwt = http_cerver_auth_jwt_new ()
	if (http_jwt):
		http_cerver_auth_jwt_add_value_int (http_jwt, b"iat", int (time.time ()))
		http_cerver_auth_jwt_add_value (http_jwt, b"id", str (user.id).encode ("utf-8"))
		http_cerver_auth_jwt_add_value (http_jwt, b"email", user.email.encode ("utf-8"))
		http_cerver_auth_jwt_add_value (http_jwt, b"name", user.name.encode ("utf-8"))
		http_cerver_auth_jwt_add_value (
			http_jwt, b"role", percepthor_role_get_name_by_oid (user.role).encode ("utf-8")
		)
		http_cerver_auth_jwt_add_value (http_jwt, b"username", user.username.encode ("utf-8"))

		# TODO: add first time value
		if (not http_cerver_auth_generate_bearer_jwt_json (
			http_receive_get_cerver (http_receive), http_jwt
		)):
			result = ctypes.create_string_buffer (
				http_jwt_get_json (http_jwt),
				HTTP_JWT_TOKEN_SIZE
			)

		http_cerver_auth_jwt_delete (http_jwt)

	if (result is None):
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def percepthor_user_login_validate_input (loaded_json, errors):
	values = {}

	values["email"] = validate_body_email_value (loaded_json, "email", errors)
	values["password"] = validate_body_value_exists (loaded_json, "password", errors)

	return values

def percepthor_user_login_internal (http_receive, loaded_json):
	error = SERVICE_ERROR_NONE
	errors = {}
	token = None

	values = percepthor_user_login_validate_input (loaded_json, errors)

	if (not errors):
		found = percepthor_user_get_for_login (values["email"])
		if (found):
			if (found.password == values["password"]):
				cerver_log_success (
					f"User {found.email} logged in!".encode ("utf-8")
				)

				error, token = percepthor_user_generate_token (
					http_receive, found
				)

			else:
				cerver_log_error (
					f"User {found.email} bad password!".encode ("utf-8")
				)

				errors["password"] = "Password is incorrect!"

				error = SERVICE_ERROR_BAD_REQUEST

		else:
			errors["email"] = f"User with email was {values['email']} not found!"
			error = SERVICE_ERROR_NOT_FOUND

	else:
		error = SERVICE_ERROR_MISSING_VALUES

	return error, errors, token

# TODO: update last time!
def percepthor_user_login (http_receive, body_json):
	error = SERVICE_ERROR_NONE
	errors = {}
	token = None

	if (body_json is not None):
		try:
			loaded_json = json.loads (body_json.contents.str)

			error, errors, token = percepthor_user_login_internal (
				http_receive, loaded_json
			)

		except Exception as e:
			if (percepthor.RUNTIME == runtime.RUNTIME_TYPE_DEVELOPMENT):
				print (e)

			error = SERVICE_ERROR_BAD_REQUEST

	else:
		error = SERVICE_ERROR_BAD_REQUEST

	return error, errors, token

def percepthor_user_register_validate_input (loaded_json, errors):
	values = {}

	values["name"] = validate_body_value (loaded_json, "name", 1, 128, errors)
	values["email"] = validate_body_email_value (loaded_json, "email", errors)
	values["username"] = validate_body_value (loaded_json, "username", 1, 64, errors)

	values["password"] = validate_body_password_match (
		loaded_json, "password", "confirm", errors
	)

	return values

def percepthor_user_register_internal (http_receive, loaded_json):
	error = SERVICE_ERROR_NONE
	errors = {}
	token = None

	values = percepthor_user_register_validate_input (loaded_json, errors)

	if (not errors):
		# TODO: check if username exists
		found = percepthor_user_check_by_email (values["email"])
		if (not found):
			user = user_create (
				values["email"], values["name"],
				values["username"], values["password"]
			)

			percepthor_user_set_role (user, "common")

			user_id = user_insert (user)

			cerver_log_success (b"Created a new user!")

			# TODO: send confirmation email

			error, token = percepthor_user_generate_token (
				http_receive, user_id
			)

		else:
			cerver_log_warning (
				f"User {values['email']} already exists!".encode ("utf-8")
			)

			errors["email"] = f"Email has already been registered"

			error = SERVICE_ERROR_BAD_REQUEST

	else:
		error = SERVICE_ERROR_MISSING_VALUES

	return error, errors, token

def percepthor_user_register (http_receive, body_json):
	error = SERVICE_ERROR_NONE
	errors = {}
	token = None

	if (body_json is not None):
		try:
			loaded_json = json.loads (body_json.contents.str)

			error, errors, token = percepthor_user_register_internal (
				http_receive, loaded_json
			)

		except Exception as e:
			if (percepthor.RUNTIME == runtime.RUNTIME_TYPE_DEVELOPMENT):
				print (e)

			error = SERVICE_ERROR_BAD_REQUEST

	else:
		error = SERVICE_ERROR_BAD_REQUEST

	return error, errors, token
