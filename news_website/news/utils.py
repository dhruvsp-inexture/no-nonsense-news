import random
import string


def allowed_file(filename):
    """function for allowing specific file extension to be accepted

    Parameters
    ----------
    filename: str
        name of the file whose extensions are needed to be checked
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    if filename:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    else:
        return True


def get_random_alphanumeric_string(length):
    """function for generating random alphanumeric string which is supposed to be used as prefix in the name of the
    image file

    Parameters
    ----------
    length: int
        length of the prefix which is added to the name of the image file
    """
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
