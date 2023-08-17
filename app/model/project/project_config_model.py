class ProjectConfig:
    ANSWER_TYPE_TEXT = "text"
    ANSWER_TYPE_CHOICE = "choice"
    ANSWER_TYPE_IMAGE = "image"

    title: str
    description: str
    question_title: str
    question_content_fields: list[str]
    question_field: str
    answer_type: str
    repeated_tasks: int
    password: str
    placeholder_field: str
    answer_choice: dict[str, str]
    random_sampling: bool

    def __init__(self,
                 title: str,
                 description: str,
                 answer_type: str,
                 repeated_tasks: int,
                 password: str,
                 question_title: str = "",
                 random_sampling: bool = False,
                 question_field: str = "",
                 question_content_fields: list[str] = [],
                 placeholder_field: str = None,
                 answer_choice: dict[str, str] = None):
        self.title = title
        self.description = description
        self.question_title = question_title
        self.question_content_fields = question_content_fields
        self.question_field = question_field
        self.answer_type = answer_type
        self.repeated_tasks = repeated_tasks
        self.password = password
        self.random_sampling = random_sampling

        if answer_type == self.ANSWER_TYPE_CHOICE and answer_choice is None:
            raise KeyError("Type answer 'choice' need answer_choice options")
        self.placeholder_field = placeholder_field
        self.answer_choice = answer_choice
