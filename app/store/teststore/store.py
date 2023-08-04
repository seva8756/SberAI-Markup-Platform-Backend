from app.store.teststore.repositories.projectrepository.project_repository import ProjectRepository
from app.store.teststore.repositories.tokenrepository.token_repository import TokenRepository
from app.store.teststore.repositories.userrepository.user_repository import UserRepository


class Store:
    user_repository: UserRepository = None
    token_repository: TokenRepository = None
    project_repository: ProjectRepository = None

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

    def Project(self) -> ProjectRepository:
        if self.project_repository is not None:
            return self.project_repository

        self.project_repository = ProjectRepository(self, {}, {}, [])
        return self.project_repository
