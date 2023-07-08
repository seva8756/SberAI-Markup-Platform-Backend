from .user import User


def TestUser(email="user@example.org", password="password") -> User:
    u = User()
    u.Email = email
    u.Password = password
    return u
