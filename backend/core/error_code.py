class ErrorCode:
    ERR_UNAUTHORIZED = "UNAUTHORIZED"
    ERR_ACCESS_DENIED = "ACCESS_DENIED"
    ERR_INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

    ERR_NOT_FOUND = "NOT_FOUND"
    ERR_NOT_EDITABLE = "NOT_EDITABLE"
    ERR_EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    ERR_USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    ERR_REQUEST_BODY_INVALID = "REQUEST_BODY_INVALID"
    ERR_USER_NOT_FOUND = "USER_NOT_FOUND"
    ERR_USER_NOT_VERIFIED = "USER_NOT_VERIFIED"
    ERR_INVALID_NEW_EMAIL = "INVALID_NEW_EMAIL"

    ERR_PASSWORDS_NOT_MATCHING = "PASSWORDS_NOT_MATCHING"
    ERR_TOKEN_EXPIRED = "TOKEN_EXPIRED"
    ERR_INVALID_REFRESH_TOKEN = "INVALID_REFRESH_TOKEN"
    ERR_TOKEN_INVALID = "TOKEN_INVALID"
    ERR_INVALID_PASSWORD = "INVALID_PASSWORD"
    ERR_INVALID_URL = "INVALID_URL"
    ERR_INVALID_PHONE = "INVALID_PHONE"

    ERR_USER_ALREADY_DELETED = "USER_ALREADY_DELETED"
    


class ErrorMessage:
    ERR_INVALID_PASSWORD = "Password must be at least 8 characters long"
    ERR_INVALID_PASSWORD_WIDTH = "Password must be halfwidth alphanumeric characters"
    ERR_PASSWORDS_NOT_MATCHING = "New password and confirm password are not same"
    ERR_INVALID_URL = "URL must start with http or https"
    ERR_INVALID_PHONE = "Invalid phone number"
    ERR_INVALID_PHONE_LENGTH = "Phone number must be 11 digits long"
    ERR_EMAIL_ALREADY_EXISTS = "メールアドレスが既に存在します。"
    ERR_DISH_NOT_FOUND = "This dish doesn't exist"
    ERR_USER_NOT_FOUND = "This user doesn't exist"
