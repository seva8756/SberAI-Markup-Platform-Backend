from typing import Dict

import app.store as store
from app.model.token.token_model import Token
from app.store.errors import ErrRecordNotFound
from app.store.store import Store

Sessions = Dict[int, Token]


class TokenRepository(store.TokenRepository):
    store: Store
    sessions: Sessions

    def __init__(self, store: Store, sessions: Sessions):
        self.store = store
        self.sessions = sessions

    def Create(self, t: Token) -> Exception:
        t.ID = len(self.sessions) + 1
        self.sessions[t.ID] = t
        pass

    def Update(self, t: Token) -> Exception:
        if not hasattr(t, "ID"):
            return AttributeError("Token has no ID")
        self.sessions[t.ID].refresh_token = t.refresh_token

    def FindByRefresh(self, refresh: str) -> (Token, Exception):
        for t in self.sessions.values():
            if t.refresh_token == refresh:
                return t, None
        return None, ErrRecordNotFound

    def Reset(self, refresh: str) -> Exception:
        for t in self.sessions.values():
            if t.refresh_token == refresh:
                del self.sessions[t.ID]
                return None
        return ErrRecordNotFound
