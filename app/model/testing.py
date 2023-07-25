from app.model.token.token_model import Token
from app.model.user.user_model import User
from app.service.token_service import TokenService


def TestUser(email="user@example.org", password="password", first_name="first_name", last_name="last_name") -> User:
    u = User()
    u.email = email
    u.password = password
    u.first_name = first_name
    u.last_name = last_name
    return u


def TestToken(user=123, refresh_token="refresh_token", generate_valid=False) -> Token:
    t = Token()
    t.user = user
    if not generate_valid:
        t.refresh_token = refresh_token
    else:
        t.refresh_token = TokenService.generate_tokens(user)["refresh_token"]
    return t
