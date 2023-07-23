import bcrypt
from cerberus import Validator


class User:
    ID: int
    Email: str = ""
    Password: str = ""
    EncryptedPassword: str = ""

    def Validate(self) -> (bool, Exception):
        v = Validator({
            'Email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                'required': True
            },
            'Password': {
                'type': 'string',
                'required': self.EncryptedPassword == "",
                'empty': self.EncryptedPassword != "",
                'minlength': 6, 'maxlength': 100
            }
        }, allow_unknown=True)
        res = v.validate(vars(self))
        if len(v.errors) > 0:
            return None, Exception(v.errors)
        return res, None

    def BeforeCreate(self) -> Exception:
        if len(self.Password) > 0:
            (enc, err) = self._encryptString(self.Password)
            if err is not None:
                return err

            self.EncryptedPassword = enc

    def ComparePassword(self, password):
        return bcrypt.checkpw(password, self.EncryptedPassword)

    def GetClientData(self):
        return {"ID": self.ID}

    def _encryptString(self, s: str) -> (str, Exception):
        try:
            b = bcrypt.hashpw(s, bcrypt.gensalt(12))
        except Exception as err:
            return None, err
        return b, None
