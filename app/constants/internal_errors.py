from enum import Enum


class InternalErrorCode(Enum):
    InvalidProvider = (1001, "Invalid Provider",
                       "Unsupported oauth provider selected.")
    BotNotExist = (1002, "No bot exist",
                   "Bot with given information does not exist")

    def __init__(self, code: int, description: str, message: str):
        self._code = code
        self._description = description
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def description(self):
        return self._description

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f"{self._code}({self._description}):{self._description}"

    def get_code(self):
        return self._code
    
    def get_description(self):
        return self._description
    
    def get_message(self):
        return self._message