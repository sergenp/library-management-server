import toml

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
CONFIG = toml.load("./config.toml")
UPLOAD_FOLDER = "/".join(CONFIG.get("file").get("path"))

def check_image(image_name):
    print(image_name)
    if '.' in image_name and \
           image_name.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
        return f"{uuid.uuid1()}.{image_name.split('.')[1]}"
    else:
        return ""

def date_type(x): return datetime.strptime(x, '%d/%m/%Y')
