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
            "INSERT INTO users (email, encrypted_password, firstName, lastName, reg_ip) VALUES (%s, %s, %s, %s, %s)",
            u.email,
            u.encrypted_password,
            u.first_name,
            u.last_name,
            u.ip)
        if err is not None:
            if err.errno == errorcode.ER_DUP_ENTRY:
                return ErrRecordAlreadyExist
            return err

        u.ID = info.last_row_id

    def FindByEmail(self, email: str) -> (User, Exception):
        res, err, _ = self.store.query("SELECT * FROM users WHERE email = %s",
                                       email, one=True)
        if err is not None:
            return None, err
        if res is None:
            return None, ErrRecordNotFound

        u = User()
        u.ID = res["ID"]
        u.email = res["email"]
        u.first_name = res["firstName"]
        u.last_name = res["lastName"]
        u.encrypted_password = res["encrypted_password"]
        u.is_admin = bool(res["isAdmin"])
        u.reg_date = res["reg_date"]
        return u, None

    def Find(self, id: int) -> (User, Exception):
        res, err, _ = self.store.query("SELECT * FROM users WHERE ID = %s",
                                       id, one=True)
        if err is not None:
            return None, err
        if res is None:
            return None, ErrRecordNotFound

        u = User()
        u.ID = res["ID"]
        u.email = res["email"]
        u.first_name = res["firstName"]
        u.last_name = res["lastName"]
        u.encrypted_password = res["encrypted_password"]
        u.is_admin = bool(res["isAdmin"])
        u.reg_date = res["reg_date"]
        return u, None
