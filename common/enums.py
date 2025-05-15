from enum import Enum


class ExperienceType(Enum):
    PROGRAM_LANGUAGE = 1
    NET_WORK = 2
    OS = 3
    DATABASE = 4
    DB_CONSTRUCTION_PROCESS = 5
    SYSTEM_REQUIREMENTS = 6
    BUSINESS_KNOWLEDGE = 7
    FRAMEWORK = 8
    TOOLS = 9
    PROCESS = 10


class UserStatus(Enum):
    EDITING = 1
    DISABLED = 2
    MAKEUP_DONE = 3
    APPROVED = 4

    @classmethod
    def items(cls):
        return [(item.value, item.name) for item in cls]
