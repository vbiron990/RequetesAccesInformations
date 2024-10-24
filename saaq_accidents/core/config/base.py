import os

import git
import yaml

from core.logger.base import logger


class Config:
    __config_name__ = None
    __section_name__ = None

    def __init__(self):
        pass

    @classmethod
    def get_config_by_name(cls, name):
        """"""
        data = None
        git_repo = git.Repo(os.path.abspath(__file__), search_parent_directories=True)
        dirname = git_repo.git.rev_parse("--show-toplevel")

        config_file = os.path.join(
            dirname,
            ".config",
            cls.__config_name__
        )

        if not os.path.exists(config_file):
            raise ExceptionGroup(".config folder or config file doest not exist.")

        with open(config_file, "r") as stream:
            try:
                data = (yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                logger.error(exc)
        if data:
            return data.get(cls.__section_name__).get(name)


class DatabaseAPIKeysConfig(Config):
    __config_name__ = "database.yaml"
    __section_name__ = "database"

    URL = "url"
    DB_NAME = "database_name"
