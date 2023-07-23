from app.model.token.token_model import Token
from app.model.user.user_model import User
from app.service.token_service import TokenService


def TestUser(email="user@example.org", password="password") -> User:
    u = User()
    u.Email = email
    u.Password = password
    return u


def TestToken(user=123, refresh_token="refresh_token", generate_valid=False) -> Token:
    t = Token()
    t.user = user
    if not generate_valid:
        t.refresh_token = refresh_token
    else:
        t.refresh_token = TokenService.generateTokens(user)["refresh_token"]
    return t
