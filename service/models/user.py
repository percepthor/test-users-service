import datetime

from bson import json_util
from bson.objectid import ObjectId

users = None

user_check_select = {
	"email": 1
}

user_login_select = {
	"email": 1,
	"name": 1,
	"username": 1,
	"password": 1,

	"role": 1
}

user_public_profile_select = {
	"name": 1,
	"username": 1,

	"member_since": 1,
	"last_time": 1,

	"bio": 1,
	"location": 1,
	"avatar": 1
}

user_account_select = { 
	"email": 1,
	"name": 1,
	"username": 1,

	"member_since": 1,
	"last_time": 1,

	"bio": 1,
	"location": 1,
	"avatar": 1,

	"role": 1
}

def user_model_init (db):
	global users
	users = db["users"]

class User ():
	def __init__ (self):
		self.oid = None
		self.id = None

		self.email = None
		self.name = None
		self.username = None
		self.password = None

		self.confirmation = False
		self.confirmation_token = None

		self.reset_password_token = None
		self.reset_password_expires = None

		self.member_since = None
		self.last_time = None

		self.bio = None
		self.location = None
		self.avatar = "no-avatar.jpg"

		self.role = None

		self.iat = 0

	def __str__ (self):
		return f"User: \n\t{self.id} \n\t{self.username} \n\t{self.role}"

# creates a new user
def user_create (email, name, username, password) -> User:
	user = User ()

	user.email = email
	user.name = name
	user.username = username
	user.password = password

	user.confirmation = False

	user.member_since = datetime.datetime.utcnow ()
	user.last_time = datetime.datetime.utcnow ()

	return user

def user_parse (user_values: dict) -> User:
	user = User ()

	user.oid = user_values["_id"]
	user.id = str (user.oid)

	user.email = user_values["email"]
	user.name = user_values["name"]
	user.username = user_values["username"]
	user.password = user_values["password"]

	user.role = user_values["role"]
	
	return user

def user_load (email, iat, id, name, role, username):
	user = User ()

	user.id = id

	user.email = email
	user.name = name
	user.role = role
	user.username = username

	user.iat = iat

	return user

def user_get_by_id (id: str, select: dict):
	return users.find_one ({"_id": ObjectId (id)}, select)

def user_get_by_id_to_json (id: str, select: dict):
	result = None
	found = users.find_one (
		{ "_id": ObjectId (id) },
		select
	)

	if (found):
		result = json_util.dumps (found)

	return result

def user_get_by_email (email: str, select: dict):
	return users.find_one ({"email": email}, select)

def user_insert (user):
	user.id = users.insert ({
		"email": user.email,
		"name": user.name,
		"username": user.username,
		"password": user.password,

		"confirmation": user.confirmation,
		"confirmation_token": user.confirmation_token,

		"reset_password_token": user.reset_password_token,
		"reset_password_expires": user.reset_password_expires,

		"member_since": user.member_since,
		"last_time": user.last_time,

		"bio": user.bio,
		"location": user.location,
		"avatar": user.avatar,

		"role": user.role
	})

	return user

def user_update (user_id: str, update: dict) -> bool:
	result = False

	updated = users.update_one (
		{"_id": ObjectId (user_id)},
		{
			"$set": update
		}
	)

	if (updated.modified_count):
		result = True

	return result

def user_delete (user_id: str):
	result = False

	updated = users.delete_one (
		{"_id": ObjectId (user_id)}
	)

	if (updated.deleted_count):
		result = True

	return result
