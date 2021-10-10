ALLOWED_EXTENSIONS = ['png']


def check_ext(filename):
    ext = filename.rsplit('.', 1)[1]
    return ext.lower() in ALLOWED_EXTENSIONS
