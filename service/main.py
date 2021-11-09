import signal

import cerver

from db import percepthor_mongo_init
from percepthor import percepthor_config, percepthor_init
import service
import version

if __name__ == "__main__":
	signal.signal (signal.SIGINT, service.end)
	signal.signal (signal.SIGTERM, service.end)
	signal.signal (signal.SIGPIPE, signal.SIG_IGN)

	cerver.cerver_init ()

	cerver.cerver_version_print_full ()

	cerver.pycerver_version_print_full ()

	version.users_service_version_print_full ()

	percepthor_config ()

	if (percepthor_mongo_init ()):
		percepthor_init ()

		service.start ()
