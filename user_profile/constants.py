
class Error:
    USER_INACTIVE = "User is not active."
    SOMETHING_HAPPENED = "Something bad happend."
    USER_EMAIL_EXIST = "User with this email already exist."
    PASSWORD_MATCHING_ERROR = "Passwords do not match."
    LOGIN_ERROR = "Email or Password is invalid.."


class Succes:
    OK = "Ok"
    USER_REGISTER = "User has been registered."
    LOGIN_SUCCESS = "Login successfull."
    LOGOUT_SUCCESS = "Logout succesfull."

class URL:
    LOGIN = "/auth/flog/login"
    SIGNUP = "/auth/flog/register"