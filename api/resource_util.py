import toml
import re
from datetime import datetime
import uuid

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
CONFIG = toml.load("./config.toml")
UPLOAD_FOLDER = "/".join(CONFIG.get("file").get("path"))
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def check_image(image_name):
    if '.' in image_name and \
            image_name.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
        return f"{uuid.uuid1()}.{image_name.split('.')[1]}"
    else:
        return ""


def date_type(x):
    return datetime.strptime(x, '%d/%m/%Y')


def email_type(x):
    if re.search(EMAIL_REGEX, x):
        return x
    raise ValueError("Invalid email")
