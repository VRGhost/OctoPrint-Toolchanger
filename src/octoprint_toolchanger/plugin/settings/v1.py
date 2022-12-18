from . import base


class V1Settings(base.BoundSettings):
    """V1 settings"""

    @classmethod
    def get_version(cls) -> int:
        return 1

    @classmethod
    def get_defaults(cls) -> dict:
        return {}

    @classmethod
    def get_restricted_paths(cls):
        return {}
