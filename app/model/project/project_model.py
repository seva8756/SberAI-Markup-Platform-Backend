from pandas import DataFrame

from app.model.project.project_config_model import ProjectConfig
from app.utils import utils


class Project:
    ID: int
    directory: int
    closed: bool = False
    csv: DataFrame
    config: ProjectConfig = {}

    def get_general_information(self):
        data = {
            "ID": self.ID,
            "code": utils.ProjectCode.encode_id(self.ID),
            "title": self.config.title,
            "description": self.config.description,
            "question_title": self.config.question_title,
            "answer_type": self.config.answer_type,
        }
        if self.config.answer_type == self.config.ANSWER_TYPE_CHOICE:
            data["answer_choice"] = self.config.answer_choice
        return data
