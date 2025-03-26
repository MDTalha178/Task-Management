class CustomError:
    # Generic error messages
    REQUIRED_FIELD = "This field is required."
    BLANK_FIELD = "This field cannot be blank."
    INVALID_FIELD = "Invalid value."

    # Signup-specific error messages
    NAME_REQUIRED = "Name cannot be blank."
    EMAIL_REQUIRED = "Email address is required."
    PASSWORD_BLANK = "Password cannot be blank."
    PASSWORD_REQUIRED = "Password is required."
    # Optional: You can add more specific error messages or categorize them

    PHONE_FORMAT_INVALID = "Phone number is not in a valid format."
    EMAIL_INVALID = "Email address is invalid."
    EMAIL_ALREADY_EXISTS = 'Email already exists!'

    # Here are some default message
    SERVER_NOT_RESPONDING = 'Server not responding'
    SERVER_NOT_ABLE_PROCESS_REQUEST = 'Not able to process your request at this moment.please try after some time'
    SOMETHING_WENT_WRONG = "Oops! Something went wrong."

    # AUTH Message
    INVALID_EMAIL = 'Email not exists in our system'

    # Views validation
    USER_ID_REQUIRED = 'User ID is required to fetch a specific user task details'

    @staticmethod
    def get_error_message(error_key):
        """
        This method allows dynamic access to error messages by their keys.
        Example: CustomError.get_error_message('FIRST_NAME_REQUIRED')
        """
        return getattr(CustomError, error_key, "Unknown error.")
