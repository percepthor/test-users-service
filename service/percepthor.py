import os

from errors import service_errors_end
from runtime import *

from controllers.roles import percepthor_roles_init

RUNTIME = runtime_from_string (os.environ.get ("RUNTIME"))

PORT = int (os.environ.get ("PORT"))

CERVER_RECEIVE_BUFFER_SIZE = int (os.environ.get ("CERVER_RECEIVE_BUFFER_SIZE"))
CERVER_TH_THREADS = int (os.environ.get ("CERVER_TH_THREADS"))
CERVER_CONNECTION_QUEUE = int (os.environ.get ("CERVER_CONNECTION_QUEUE"))

MONGO_APP_NAME = os.environ.get ("MONGO_APP_NAME")
MONGO_DB = os.environ.get ("MONGO_DB")
MONGO_URI = os.environ.get ("MONGO_URI")

PRIV_KEY = os.environ.get ("PRIV_KEY")
PUB_KEY = os.environ.get ("PUB_KEY")

def percepthor_config ():
	print ("RUNTIME: ", runtime_to_string (RUNTIME))

	print ("PORT: ", PORT)

	print ("CERVER_RECEIVE_BUFFER_SIZE: ", CERVER_RECEIVE_BUFFER_SIZE)
	print ("CERVER_TH_THREADS: ", CERVER_TH_THREADS)
	print ("CERVER_CONNECTION_QUEUE: ", CERVER_CONNECTION_QUEUE)

	print ("MONGO_APP_NAME: ", MONGO_APP_NAME)
	print ("MONGO_DB: ", MONGO_DB)
	# print ("MONGO_URI: ", MONGO_URI)

	print ("PRIV_KEY: ", PRIV_KEY)
	print ("PUB_KEY: ", PUB_KEY)

def percepthor_init ():
	percepthor_roles_init ()

def percepthor_end ():
	service_errors_end ()
