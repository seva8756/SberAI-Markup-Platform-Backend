from app.store.teststore.repositories.tokenrepository.token_repository import TokenRepository
from app.store.teststore.repositories.userrepository.user_repository import UserRepository


class Store:
    user_repository: UserRepository = None
    token_repository: TokenRepository = None

    def User(self) -> UserRepository:
        if self.user_repository is not None:
            return self.user_repository

        self.user_repository = UserRepository(self, {})
        return self.user_repository

    def Token(self) -> TokenRepository:
        if self.token_repository is not None:
            return self.token_repository

        self.token_repository = TokenRepository(self, {})
        return self.token_repository
