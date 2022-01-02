from hamlet.backend.common.exceptions import BackendException


class TaskConditionFailureException(BackendException):
    pass


class TaskFailureException(BackendException):
    pass
