from models.role import *

roles = []

def percepthor_roles_init ():
	global roles
	roles = roles_get_all ()

def percepthor_role_get_by_oid (oid):
	for role in roles:
		if (role.oid == oid):
			return role

	return None

def percepthor_role_get_name_by_oid (oid):
	for role in roles:
		if (role.oid == oid):
			return role.name

	return None

def percepthor_role_get_by_name (rolename):
	for role in roles:
		if (role.name == rolename):
			return role

	return None

def percepthor_role_check_action (role, action):
	for a in role.actions:
		if (a == action):
			return True

	return False

# gets a role by name and checks it has the action
# returns True on success, False on error
def percepthor_roles_search_and_check_action (
	rolename, action
):
	for role in roles:
		if (role.name == rolename):
			for a in role.actions:
				if (a == action):
					return True

	return False
