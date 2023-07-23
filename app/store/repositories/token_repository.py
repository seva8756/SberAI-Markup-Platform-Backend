from abc import abstractmethod
from app.model import User
from app.model.token.token_model import Token


class TokenRepository:

    @abstractmethod
    def Create(self, t: Token) -> Exception:
        pass

    @abstractmethod
    def Update(self, t: Token) -> Exception:
        pass

    @abstractmethod
    def FindByRefresh(self, refresh: str) -> (Token, Exception):
        pass

    @abstractmethod
    def Reset(self, refresh: str) -> Exception:
        pass
