import base64

from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def get_image_in_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


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
        decoded_id = 0
        for char in code[len(ProjectCode.prefix):]:  # Пропускаем первые три символа "PRJ"
            decoded_id = decoded_id * len(ProjectCode.digits) + ProjectCode.digits.index(char) + 1

        return decoded_id
