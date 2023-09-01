from pandas import DataFrame

from app.model.project.project_config_model import ProjectConfig
from app.utils import utils


class Project:
    ID: int
    directory: str
    closed: bool = False
    csv: DataFrame
    config: ProjectConfig = {}

    def get_general_information(self):
        data = {
            "ID": self.ID,
            "code": utils.ProjectCode.encode_id(self.ID),
            "title": self.config.title,
            "description": self.config.description,
            "instruction": self.config.instruction,
            "question_title": self.config.question_title,
            "components": self.config.components
        }
        return data
