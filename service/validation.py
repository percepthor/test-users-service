from cerver.http import validate_body_value_exists

from email_validator import validate_email, EmailNotValidError

import percepthor
import runtime

def validate_body_email_value (body, value, errors):
	email = validate_body_value_exists (body, value, errors)

	if (email):
		try:
			valid = validate_email (
				body[value],
				check_deliverability=True,
                allow_smtputf8=True,
                allow_empty_local=False,
			)

			# update with the normalized form
			email = valid.email
		except EmailNotValidError as e:
			# email is not valid
			if (percepthor.RUNTIME == runtime.RUNTIME_TYPE_DEVELOPMENT):
				print (str (e))

			errors[value] = f"Field {value} is an invalid email."

	return email

def validate_body_password_match (
	body, pswd_value, confirm_value, errors
):
	result = None

	password = validate_body_value_exists (body, pswd_value, errors)
	confirm = validate_body_value_exists (body, confirm_value, errors)

	if (password and confirm):
		if (password == confirm):
			result = password

		else:
			errors[confirm_value] = f"Passwords do not match."

	return result
