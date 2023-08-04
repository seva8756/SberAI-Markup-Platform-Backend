class ProjectConfig:
    ANSWER_TYPE_TEXT = "text"
    ANSWER_TYPE_CHOICE = "choice"

    title: str
    description: str
    question_title: str
    question_fields: str
    answer_type: str
    repeated_tasks: int
    password: str
    placeholder_fields: str
    answer_choice: dict[str, str]

    def __init__(self,
                 title: str,
                 description: str,
                 question_title: str,
                 question_fields: str,
                 answer_type: str,
                 repeated_tasks: int,
                 password: str,
                 placeholder_fields: str = None,
                 answer_choice: dict[str, str] = None):
        self.title = title
        self.description = description
        self.question_title = question_title
        self.question_fields = question_fields
        self.answer_type = answer_type
        self.repeated_tasks = repeated_tasks
        self.password = password

        if answer_type == self.ANSWER_TYPE_CHOICE and answer_choice is None:
            raise KeyError("Type answer 'choice' need answer_choice options")
        self.placeholder_fields = placeholder_fields
        self.answer_choice = answer_choice

