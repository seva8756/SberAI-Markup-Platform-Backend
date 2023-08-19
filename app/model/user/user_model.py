import datetime

import bcrypt
from cerberus import Validator

from app.controllers import errors


class User:
    ID: int
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
    is_admin: bool = False
    encrypted_password: str = ""
    reg_date: datetime.datetime
    ip: str = ""

    def Validate(self) -> (bool, Exception):
        v = Validator({
            'email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                'required': True,
                'maxlength': 100
            },
            'password': {
                'type': 'string',
                'required': self.encrypted_password == "",
                'empty': self.encrypted_password != "",
                'minlength': 6, 'maxlength': 100
            },
            'first_name': {
                'type': 'string',
                'required': True,
                'empty': False,
                'minlength': 1, 'maxlength': 50
            },
            'last_name': {
                'type': 'string',
                'required': True,
                'empty': False,
                'minlength': 1, 'maxlength': 50
            }
        }, allow_unknown=True)
        res = v.validate(vars(self))
        if len(v.errors) > 0:
            errors.errUserNotPassValidation.message = v.errors
            return None, errors.errUserNotPassValidation
        return res, None

    def BeforeCreate(self) -> Exception:
        if len(self.password) > 0:
            (enc, err) = self._encryptString(self.password)
            if err is not None:
                return err

            self.encrypted_password = enc

    def ComparePassword(self, password) -> bool:
        try:
            return bcrypt.checkpw(password, self.encrypted_password)
        except Exception:
            return False

    def GetClientData(self):
        return {
            "ID": self.ID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "email": self.email,
            "reg_date": self.reg_date
        }

    def _encryptString(self, s: str) -> (str, Exception):
        try:
            b = bcrypt.hashpw(s, bcrypt.gensalt(12))
        except Exception as err:
            return None, err
        return b, None
