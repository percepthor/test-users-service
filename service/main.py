import signal

import cerver

import service
from config import service_config
import version

if __name__ == "__main__":
	signal.signal (signal.SIGINT, service.end)
	signal.signal (signal.SIGTERM, service.end)
	signal.signal (signal.SIGPIPE, signal.SIG_IGN)

	cerver.cerver_init ()

	cerver.cerver_version_print_full ()

	cerver.pycerver_version_print_full ()

	version.users_service_version_print_full ()

	service_config ()

	service.start ()
