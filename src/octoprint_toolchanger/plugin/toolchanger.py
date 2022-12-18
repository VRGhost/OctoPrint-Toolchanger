import octoprint.plugin

from . import settings


class Toolchanger(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.AssetPlugin,
):
    """The Octoprint plugin interface class"""

    bound_settings_cls = settings.v1.V1Settings
    bound_settings: settings.v1.V1Settings = None

    def on_settings_migrate(self, target, current):
        raise NotImplementedError

    def get_settings_version(self) -> int:
        return self.bound_settings_cls.get_version()

    def get_settings_defaults(self) -> dict:
        return self.bound_settings_cls.get_defaults()

    def get_settings_restricted_paths(self) -> dict:
        return self.bound_settings_cls.get_restricted_paths()

    def on_settings_initialized(self):
        self.bound_settings = self.bound_settings_cls(self._settings)

    def get_update_information(self):
        from .. import __VERSION__, __plugin_name__

        return {
            "psucontrol_meross": {
                "displayName": __plugin_name__,
                "displayVersion": __VERSION__,
                "current": __VERSION__,
                # version check: github repository
                "type": "github_release",
                "user": "VRGhost",
                "repo": "OctoPrint-Toolchanger",
                "stable_branch": {
                    "name": "Stable",
                    "branch": "main",
                },
                "prerelease_branches": [
                    {
                        "name": "Prerelease",
                        "branch": "main",
                    }
                ],
                "prerelease": False,
                "prerelease_channel": "main",
                # update method: pip w/ dependency links
                "pip": "https://github.com/VRGhost/OctoPrint-Toolchanger/releases/download/"
                "{target_version}/OctoPrint_Toolchanger-{target_version}-py3-none-any.whl",
            }
        }
