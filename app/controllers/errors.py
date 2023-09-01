from app.errors import ServerException

errProcessing = ServerException("errProcessing", "Processing error")

errInvalidJsonData = ServerException("errInvalidJsonData", "Invalid JSON data")
errInvalidJsonFormat = ServerException("errInvalidJsonFormat", "Invalid JSON format")

errUserNotFound = ServerException("errUserNotFound", "User not found")
errUserNotPassValidation = ServerException("errUserNotPassValidation", "User did not pass validation")
errUserAlreadyRegistered = ServerException("errUserAlreadyRegistered", "User already registered")
errIncorrectEmailOrPassword = ServerException("errIncorrectEmailOrPassword", "Incorrect email or password")
errNotAuthenticated = ServerException("errNotAuthenticated", "Not authenticated")
errSessionNotFound = ServerException("errSessionNotFound", "Session Not Found")

errMissingRequiredComponent = ServerException("errMissingRequiredComponent", "Missing required component")
errNoAccessToTask = ServerException("errNoAccessToTask", "No access to task")
errNoTasksAvailable = ServerException("errNoTasksAvailable", "No tasks available in this project")
errAnswerOptionDoesNotExist = ServerException("errAnswerOptionDoesNotExist", "Answer option does not exist")
errTaskNotReservedForUser = ServerException("errTaskNotReservedForUser", "Task is not reserved for user")
errTaskNotFound = ServerException("errTaskNotFound", "Task not found")
errProjectNotFound = ServerException("errProjectNotFound", "Project not found")
errAlreadyInProject = ServerException("errAlreadyInProject", "Already in the project")
errNoAccessToTheProject = ServerException("errNoAccessToTheProject", "No access to the project")
errWrongPassword = ServerException("errWrongPassword", "Wrong password")
errPhotoUploadFailed = ServerException("errPhotoUploadFailed", "Photo upload failed")
