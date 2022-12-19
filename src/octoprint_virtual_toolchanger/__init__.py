from importlib.metadata import version

# ATTRIBUTION:
# This plugin is a fork of standard virtual_printer plugin by
# __plugin_author__ = "Gina Häußge, based on work by Daid Braam"
# __plugin_homepage__ = (
#     "https://docs.octoprint.org/en/master/development/virtual_printer.html"
# )

__VERSION__ = version("octoprint_toolchanger")
__author__ = (
    "Ilja Orlovs <vrghost@gmail.com>, based on work by Gina Häußge & Daid Braam"
)
__license__ = "AGPLv3"
__copyright__ = (
    "Copyright (C) 2022 Ilja Orlovs - Released under terms of the AGPLv3 License"
)
__plugin_name__ = "E3D Toolchanger [Virtual Printer]"
__plugin_pythoncompat__ = ">=3.10,<4"

from .plugin import VirtualToolchangerPrinter


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = VirtualToolchangerPrinter()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.transport.serial.factory": __plugin_implementation__.virtual_printer_factory,
        "octoprint.comm.transport.serial.additional_port_names": __plugin_implementation__.get_additional_port_names,
    }
