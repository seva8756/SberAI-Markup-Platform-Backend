from typing import Dict


class ProjectConfig:
    title: str
    description: str
    question_title: str
    instruction: str
    question_field: str
    repeated_tasks: int
    password: str
    random_sampling: bool
    components: Dict[str, list[str] or str]

    def __init__(self,
                 title: str,
                 description: str,
                 repeated_tasks: int,
                 password: str,
                 components: Dict[str, str],
                 instruction: str = "",
                 question_title: str = "",
                 random_sampling: bool = False,
                 question_field: str = ""):
        self.title = title
        self.description = description
        self.question_title = question_title
        self.instruction = instruction
        self.question_field = question_field
        self.repeated_tasks = repeated_tasks
        self.password = password
        self.random_sampling = random_sampling
        self.components = components

    @staticmethod
    def is_component_require(component):
        type_condition = ComponentsPurposeTypes.is_purpose_equal(component, ComponentsPurposeTypes.PURPOSE_ANSWER)
        require_condition = "require" in component and component["require"]
        return type_condition and require_condition


class ComponentsPurposeTypes:
    PURPOSE_CONTENT = "content"
    PURPOSE_ANSWER = "answer"

    @staticmethod
    def is_purpose_equal(component: dict[str, str], type: str):
        return component["purpose"] == type


class ComponentsContentTypes:
    CONTENT_IMAGES = "images"
    CONTENT_INPUT = "input"
    CONTENT_CHOICE = "choice"
    CONTENT_IMAGE = "image"

    @staticmethod
    def is_type_equal(component: dict[str, str], type: str):
        return component["type"] == type
