from cerver.utils import LOG_TYPE_NONE, cerver_log_both

USERS_VERSION = "0.2"
USERS_VERSION_NAME = "Version 0.2"
USERS_VERSION_DATE = "09/11/2021"
USERS_VERSION_TIME = "15:48 CST"
USERS_VERSION_AUTHOR = "Erick Salas"

def users_service_version_print_full ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nUsers Service Version: %s".encode ("utf-8"),
		USERS_VERSION_NAME.encode ("utf-8")
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Release Date & time: %s - %s".encode ("utf-8"),
		USERS_VERSION_DATE.encode ("utf-8"),
		USERS_VERSION_TIME.encode ("utf-8")
	)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"Author: %s\n".encode ("utf-8"),
		USERS_VERSION_AUTHOR.encode ("utf-8")
	)

def users_service_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nUsers Service Version ID: %s\n".encode ("utf-8"),
		USERS_VERSION.encode ("utf-8")
	)

def users_service_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		"\nUsers Service Version: %s\n".encode ("utf-8"),
		USERS_VERSION_NAME.encode ("utf-8")
	)
