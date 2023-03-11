class EnvironmentException(Exception):
    pass


class NoValueException(EnvironmentException):
    pass


class LazyValueException(EnvironmentException):
    pass


class DupOperationException(LazyValueException):
    pass
