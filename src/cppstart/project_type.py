from enum import Enum


class ProjectTypeException(Exception):
    pass


class ProjectType(Enum):
    APP = 0
    LIB = 1


def project_type_from_string(s: str) -> ProjectType:
    for t in ProjectType:
        if t.name == s.upper():
            return t

    raise ProjectTypeException(f"Failed to convert '{s}' to a project type")
