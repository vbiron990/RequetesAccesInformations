"""
This module is used to declare configuration files that will be used
locally on our machines to overwrite certain parameters.

Configuration files templates are available at rev_bot/core/config/templates.
The configuration files that are taken into account are the ones stored in /rev_bot/config.

Each config file is tied with a configuration class defined in rev_bot/core/config/base.py.
Each config class must also declare the keys that are accessible in the file.

If a file is not found in /rev_bot/config, None is returned.

Below are examples of how to get overrides parameters.
"""
from core.config.base import DatabaseAPIKeysConfig
from core.logger.base import logger

if __name__ == '__main__':

    """
    CASE 1: Get database url from config
    CASE 2: Get stage_key from config
    """

    CASE = 1

    if CASE == 1:
        logger.info(DatabaseAPIKeysConfig.get_config_by_name(DatabaseAPIKeysConfig.URL))
