import base64
import imghdr
import os
from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def get_image_in_base64(image_path: str) -> (str, Exception):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8'), None
    except Exception as err:
        return None, err


def save_base64_to_file(base64_string, file_path) -> Exception:
    def is_valid_image(data):
        image_type = imghdr.what(None, h=data)
        return image_type is not None

    try:
        decoded_data = base64.b64decode(base64_string)
        if not is_valid_image(decoded_data):
            raise Exception("Not valid base64 data")
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'wb') as output_file:
            output_file.write(decoded_data)
    except Exception as err:
        return err


class ProjectCode:
    prefix = "PRJ"
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def encode_id(id):

        result = ""
        while id > 0:
            remainder = (id - 1) % len(ProjectCode.digits)
            result = ProjectCode.digits[remainder] + result
            id = (id - 1) // len(ProjectCode.digits)

        return ProjectCode.prefix + result

    @staticmethod
    def decode_id(code):
        code = code.upper()
        decoded_id = 0
        for char in code[len(ProjectCode.prefix):]:  # Пропускаем первые три символа "PRJ"
            decoded_id = decoded_id * len(ProjectCode.digits) + ProjectCode.digits.index(char) + 1

        return decoded_id
