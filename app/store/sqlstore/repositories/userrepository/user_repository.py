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

        _, err, info = self.store.query(
            "INSERT INTO users (email, encrypted_password, firstName, lastName) VALUES (%s, %s, %s, %s)",
            u.email,
            u.encrypted_password,
            u.first_name,
            u.last_name)
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
        u.email = res[0][1]
        u.first_name = res[0][2]
        u.last_name = res[0][3]
        u.encrypted_password = res[0][4]
        u.is_admin = bool(res[0][5])
        return u, None

    def Find(self, id: int) -> (User, Exception):
        res, err, _ = self.store.query("SELECT * FROM users WHERE ID = %s",
                                       id)
        if err is not None:
            return None, err
        if len(res) == 0:
            return None, ErrRecordNotFound

        u = User()
        u.ID = res[0][0]
        u.email = res[0][1]
        u.first_name = res[0][2]
        u.last_name = res[0][3]
        u.encrypted_password = res[0][4]
        u.is_admin = bool(res[0][5])
        return u, None
