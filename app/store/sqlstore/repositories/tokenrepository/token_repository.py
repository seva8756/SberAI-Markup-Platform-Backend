import app.store as store
from app.model.token.token_model import Token
from app.store.errors import ErrRecordNotFound
from app.store.store import Store


class TokenRepository(store.TokenRepository):
    store: Store

    def __init__(self, store: Store):
        self.store = store

    def Create(self, t: Token) -> Exception:
        _, err, info = self.store.query("INSERT INTO sessions (user, refresh_token) VALUES (%s, %s)",
                                        t.user,
                                        t.refresh_token)
        if err is not None:
            return err
        t.ID = info.last_row_id

    def Update(self, t: Token) -> Exception:
        if not hasattr(t, "ID"):
            return AttributeError("Token has no ID")
        _, err, _ = self.store.query("UPDATE sessions SET refresh_token = %s WHERE ID = %s",
                                     t.refresh_token,
                                     t.ID)
        if err is not None:
            return err

    def FindByRefresh(self, refresh: str) -> (Token, Exception):
        res, err, _ = self.store.query(
            "SELECT ID, user, refresh_token FROM sessions WHERE refresh_token = %s AND reseted = 0",
            refresh)
        if err is not None:
            return err
        if len(res) == 0:
            return None, ErrRecordNotFound

        t = Token()
        t.ID = res[0][0]
        t.user = res[0][1]
        t.refresh_token = res[0][2]
        return t, None

    def Reset(self, refresh: str) -> Exception:
        data, err, info = self.store.query(
            "UPDATE sessions SET reseted = 1 WHERE refresh_token = %s AND reseted = 0",
            refresh)
        if err is not None:
            return err
        if info.rows_affected == 0:
            return ErrRecordNotFound
