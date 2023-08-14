class ProjectConfig:
    ANSWER_TYPE_TEXT = "text"
    ANSWER_TYPE_CHOICE = "choice"
    ANSWER_TYPE_IMAGE = "image"

    title: str
    description: str
    question_title: str
    question_fields: list[str]
    answer_type: str
    repeated_tasks: int
    password: str
    placeholder_fields: str
    answer_choice: dict[str, str]
    random_sampling: bool

    def __init__(self,
                 title: str,
                 description: str,
                 question_title: str,
                 answer_type: str,
                 repeated_tasks: int,
                 password: str,
                 random_sampling: bool = False,
                 question_fields: list[str] = [],
                 placeholder_fields: str = None,
                 answer_choice: dict[str, str] = None):
        self.title = title
        self.description = description
        self.question_title = question_title
        self.question_fields = question_fields
        self.answer_type = answer_type
        self.repeated_tasks = repeated_tasks
        self.password = password
        self.random_sampling = random_sampling

        if answer_type == self.ANSWER_TYPE_CHOICE and answer_choice is None:
            raise KeyError("Type answer 'choice' need answer_choice options")
        self.placeholder_fields = placeholder_fields
        self.answer_choice = answer_choice
