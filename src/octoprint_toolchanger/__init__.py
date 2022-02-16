__VERSION__ = "0.0.0"
__author__ = "Ilja Orlovs <vrghost@gmail.com>"
__license__ = "MIT"
__copyright__ = (
    "Copyright (C) 2022 Ilja Orlovs - Released under terms of the AGPLv3 License"
)
__plugin_name__ = "E3D Toolchanger"
__plugin_pythoncompat__ = ">=3.10,<4"

from . import exc
from .plugin import Toolchanger


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Toolchanger()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    }
