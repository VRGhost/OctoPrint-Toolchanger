"""Base settings binding class"""

import octoprint.settings


class BoundSettings:

    backend: octoprint.settings.Settings

    def __init__(self, plugin_settings: octoprint.settings.Settings):
        self.backend = plugin_settings

    @classmethod
    def get_version(cls) -> int:
        raise NotImplementedError

    @classmethod
    def get_defaults(cls):
        """SettingsPlugin.get_settings_defaults() handler"""
        raise NotImplementedError

    @classmethod
    def get_restricted_paths(cls):
        """SettingsPlugin.get_settings_restricted_paths() handler"""
        raise NotImplementedError
