from app.model import User
import app.store as store
from app.store.errors import ErrRecordNotFound


class UserRepository(store.UserRepository):
    store = None

    def __init__(self, store):
        self.store = store

    def Create(self, u: User) -> Exception:
        _, err = u.Validate()
        if err is not None:
            return err
        err = u.BeforeCreate()
        if err is not None:
            return err

        _, err = self.store.query("INSERT INTO users (email, encrypted_password) VALUES (%s, %s)",
                                  u.Email,
                                  u.EncryptedPassword)
        if err is not None:
            return err
        res, err = self.store.query("SELECT id FROM users WHERE email = %s",
                                    u.Email)
        if err is not None:
            return err
        u.ID = res[0]

    def FindByEmail(self, email: str) -> (User, Exception):
        res, err = self.store.query("SELECT * FROM users WHERE email = %s",
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
