import http
from typing import Dict

from app.controllers.errors import errIncorrectEmailOrPassword
from .token_service import TokenService
from .. import Server
from ..model.token.token_model import Token
from ..model.user.user_model import User


class UserService:

    @staticmethod
    def login(email, password) -> (Dict[str, str], Exception):
        u, err = Server.store().User().FindByEmail(email)
        if err is not None or not u.ComparePassword(password):
            return None, errIncorrectEmailOrPassword

        tokens = TokenService.generate_tokens(u.ID)
        t = Token()
        t.user = u.ID
        t.refresh_token = tokens["refresh_token"]
        err = Server.store().Token().Create(t)
        if err is not None:
            return None, err

        return {**tokens, "user_data": u.GetClientData()}, None

    @staticmethod
    def register(email, password, fist_name, last_name) -> (Dict[str, str], Exception):
        u = User()
        u.email = email
        u.password = password
        u.first_name = fist_name
        u.last_name = last_name

        err = Server.store().User().Create(u)
        if err is not None:
            return None, err

        data, err = UserService.login(email, password)
        if err is not None:
            return None, err

        return UserService.login(email, password), None

    @staticmethod
    def refresh(refresh_token: str) -> (Dict[str, str], Exception):
        t, err = Server.store().Token().FindByRefresh(refresh_token)
        if err is not None:
            return None, err
        tokens = TokenService.generate_tokens(t.user)
        t.refresh_token = tokens["refresh_token"]

        err = Server.store().Token().Update(t)
        if err is not None:
            return None, err

        return tokens, None

    @staticmethod
    def logout(refresh_token: str) -> Exception:
        err = Server.store().Token().Reset(refresh_token)
        if err is not None:
            return err

    @staticmethod
    def get_user_info(id: int) -> (dict[str, str], Exception):
        u, err = Server.store().User().Find(id)
        if err is not None:
            return None, err

        return u.GetClientData(), None
