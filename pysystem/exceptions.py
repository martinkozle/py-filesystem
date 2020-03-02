class PySystemException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDirectoryOperationException(PySystemException):
    def __init__(self):
        super().__init__('Invalid directory operation.')


class NoSuchFileException(PySystemException):
    def __init__(self):
        super().__init__('No such file.')


class InvalidCommandSyntaxException(PySystemException):
    def __init__(self):
        super().__init__('The syntax of the command is incorrect.')


class InvalidPathException(PySystemException):
    def __init__(self):
        super().__init__('The system cannot find the path specified.')


class InvalidDirectoryNameException(PySystemException):
    def __init__(self):
        super().__init__('The directory name is invalid.')
