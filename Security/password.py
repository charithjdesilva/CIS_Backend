import re

def is_valid_password(password, new_password):
    if(password == new_password):
        # Check for at least one uppercase and one lowercase letter
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\\-]', password):
            return False

        return True
    
    return False