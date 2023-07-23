import mysql.connector
from mysql.connector import errorcode

from app.model import User
import app.store as store
from app.store.errors import ErrRecordNotFound, ErrRecordAlreadyExist
from app.store.store import Store


class UserRepository(store.UserRepository):
    store: Store

    def __init__(self, store: Store):
        self.store = store

    def Create(self, u: User) -> Exception:
        _, err = u.Validate()
        if err is not None:
            return err
        err = u.BeforeCreate()
        if err is not None:
            return err

        _, err, info = self.store.query("INSERT INTO users (email, encrypted_password) VALUES (%s, %s)",
                                        u.Email,
                                        u.EncryptedPassword)
        if err is not None:
            if err.errno == errorcode.ER_DUP_ENTRY:
                return ErrRecordAlreadyExist
            return err

        u.ID = info.last_row_id

    def FindByEmail(self, email: str) -> (User, Exception):
        res, err, _ = self.store.query("SELECT * FROM users WHERE email = %s",
                                       email)
        if err is not None:
            return None, err
        if len(res) == 0:
            return None, ErrRecordNotFound

        u = User()
        u.ID = res[0][0]
        u.Email = res[0][1]
        u.EncryptedPassword = res[0][2]
        return u, None
