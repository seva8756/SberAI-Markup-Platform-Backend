from typing import Dict

from app.model import User
import app.store as store

from app.store.errors import *
from app.store.store import Store

Users = Dict[int, User]


class UserRepository(store.UserRepository):
    store: Store
    users: Users

    def __init__(self, store: Store, users: Users):
        self.store = store
        self.users = users

    def Create(self, u: User) -> Exception:
        _, err = u.Validate()
        if err is not None:
            return err
        err = u.BeforeCreate()
        if err is not None:
            return err

        u.ID = len(self.users) + 1
        self.users[u.ID] = u

    def FindByEmail(self, email: str) -> (User, ErrRecordNotFound):
        for u in self.users.values():
            if u.Email == email:
                return u, None

        return None, ErrRecordNotFound
