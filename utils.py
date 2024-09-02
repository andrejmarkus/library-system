ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_extension(filename):
    return '.' + filename.rsplit('.', 1)[1].lower()