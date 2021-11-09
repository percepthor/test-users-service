roles = None

def role_model_init (db):
	global roles
	roles = db["roles"]

class Role ():
	def __init__ (self):
		self.oid = None
		self.id = None
		self.name = None

		self.actions = []

	def __str__ (self):
		return f"Role: \n\t{self.id} \n\t{self.name}"

def role_parse (role_values):
	role = Role ()

	role.oid = role_values["_id"]
	role.id = str (role.oid)
	role.name = role_values["name"]

	role.actions = role_values["actions"]

	return role

def roles_get_all ():
	result = []

	all_roles = roles.find ({})
	if (all_roles is not None):
		for role in all_roles:
			result.append (role_parse (role))

	return result
