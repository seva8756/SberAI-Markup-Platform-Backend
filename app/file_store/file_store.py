from app.file_store.repositories.projectrepository.project_repository import ProjectFileRepository


class FileStore:
    project_repository: ProjectFileRepository = None

    def Project(self) -> ProjectFileRepository:
        if self.project_repository is not None:
            return self.project_repository

        self.project_repository = ProjectFileRepository()
        return self.project_repository
