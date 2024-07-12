



def validate_github_username(username):
    """
    Validates the github username
    username can contains only alhpanumeric characters and -
    """
    if not username:
        return "Error: Username is required"
    
    if len(username) > 39:
        return "Error: Username can not be more than 39 characters"
    if not username.replace("-", "").isalnum():
        return "Error: Username can only contain alphanumeric characters and -"
    return None