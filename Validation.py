def validate_password(password):
    val = True

    if len(password) < 8:
        print('length should be at least 8')
        val = False

    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False

    return val


def validate_full_name(full_name):
    import re

    regex = "^[a-zA-Zа-яА-ЯёЁ ]+$"
    pattern = re.compile(regex)
    count = 0
    for sym in full_name:
        if sym == " ":
            count=count+1
    if pattern.search(full_name) is not None and count == 2:
        print(True)
        return True
    else:

        return False
