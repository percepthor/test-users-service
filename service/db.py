from cerver.utils import cerver_log_success, cerver_log_error

from pymongo import MongoClient

import percepthor
import runtime

from models.role import role_model_init
from models.user import user_model_init

percepthor_db = None

def percepthor_mongo_init ():
	global percepthor_db

	result = False

	client = MongoClient (percepthor.MONGO_URI)
	try:
		percepthor_db = client.percepthor

		percepthor_db.command ("ping")

		cerver_log_success (
			b"Mongo DB connected!"
		)

		role_model_init (percepthor_db)
		user_model_init (percepthor_db)

		result = True

	except Exception as e:
		cerver_log_error (
			b"Error connecting to Mongo DB!"
		)

		print (e)

	return result
