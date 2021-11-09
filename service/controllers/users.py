import ctypes
import json

from cerver.http import validate_body_value_exists, validate_body_value

from cerver.utils import cerver_log_warning

import percepthor
from errors import *
import runtime
from validation import *

from models.user import *

from controllers.roles import percepthor_role_get_by_name

def percepthor_user_load_from_decoded_data (decoded_data):
	json_string = ctypes.cast (decoded_data, ctypes.c_char_p)
	user_dict = json.loads (json_string.value)
	user = user_load (**user_dict)

	return user

def percepthor_user_set_role (user, role_name):
	role = percepthor_role_get_by_name (role_name)
	user.role = role.oid

def percepthor_user_check_by_id (user_id: str):
	result = False
	if (user_get_by_id (user_id, user_check_select)):
		result = True

	return result

def percepthor_user_check_by_email (email: str) -> bool:
	result = False
	if (user_get_by_email (email, user_check_select)):
		result = True

	return result

def percepthor_user_get (user_id: str) -> User:
	user = None
	found = user_get_by_id (user_id, user_login_select)
	if (found is not None):
		user = user_parse (found)

	return user

def percepthor_user_get_for_login (email: str) -> User:
	user = None
	found = user_get_by_email (email, user_login_select)
	if (found is not None):
		user = user_parse (found)

	return user
