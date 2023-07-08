from typing import Dict

from app.model import User
import app.store as store

from app.store.errors import *


class UserRepository(store.UserRepository):
    store = None
    users: Dict[str, User]

    def __init__(self, store, users: Dict[str, User]):
        self.store = store
        self.users = users

    def Create(self, u: User) -> Exception:
        _, err = u.Validate()
        if err is not None:
            return err
        err = u.BeforeCreate()
        if err is not None:
            return err
        self.users[u.Email] = u
        u.ID = len(self.users)

    def FindByEmail(self, email: str) -> (User, ErrRecordNotFound):
        if email not in self.users:
            return None, ErrRecordNotFound

        return self.users[email], None
