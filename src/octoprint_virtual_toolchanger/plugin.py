import octoprint.plugin


class VirtualToolchangerPrinter(
    octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin
):

    PORT_NAME: str = "VIRTUAL_TOOLCHANGER"

    @property
    def enabled(self):
        return self._settings.get_boolean(["enabled"])

    def get_template_configs(self):
        return [{"type": "settings", "custom_bindings": False}]

    def get_settings_defaults(self):
        return {
            "enabled": False,
            "okAfterResend": False,
            "forceChecksum": False,
            "numExtruders": 4,
            "pinnedExtruders": None,
            "includeCurrentToolInTemps": True,
            "includeFilenameInOpened": True,
            "hasBed": True,
            "hasChamber": False,
            "repetierStyleTargetTemperature": False,
            "okBeforeCommandOutput": False,
            "smoothieTemperatureReporting": False,
            "klipperTemperatureReporting": False,
            "reprapfwM114": False,
            "sdFiles": {"size": True, "longname": False, "longname_quoted": True},
            "throttle": 0.01,
            "sendWait": True,
            "waitInterval": 1.0,
            "rxBuffer": 64,
            "commandBuffer": 4,
            "supportM112": True,
            "echoOnM117": True,
            "brokenM29": True,
            "brokenResend": False,
            "supportF": False,
            "firmwareName": "RepRapFirmware for Duet 2 WiFi/Ethernet",
            "sharedNozzle": False,
            "sendBusy": False,
            "busyInterval": 2.0,
            "simulateReset": True,
            "resetLines": ["start"],
            "preparedOks": [],
            "okFormatString": "ok",
            "m115FormatString": "FIRMWARE_NAME:{firmware_name} FIRMWARE_VERSION: 3.4.4 ELECTRONICS: Duet WiFi 1.02 or later + DueX5 FIRMWARE_DATE: 2022-10-20 16:17:41",
            "m115ReportCapabilities": True,
            "capabilities": {
                "AUTOREPORT_TEMP": True,
                "AUTOREPORT_SD_STATUS": True,
                "AUTOREPORT_POS": False,
                "EMERGENCY_PARSER": True,
                "EXTENDED_M20": False,
            },
            "m114FormatString": "X:{x} Y:{y} Z:{z} E:{e[current]} Count: A:{a} B:{b} C:{c}",
            "m105TargetFormatString": "{heater}:{actual:.2f}/ {target:.2f}",
            "m105NoTargetFormatString": "{heater}:{actual:.2f}",
            "ambientTemperature": 21.3,
            "errors": {
                "checksum_mismatch": "Checksum mismatch",
                "checksum_missing": "Missing checksum",
                "lineno_mismatch": "expected line {} got {}",
                "lineno_missing": "No Line Number with checksum, Last Line: {}",
                "maxtemp": "MAXTEMP triggered!",
                "mintemp": "MINTEMP triggered!",
                "command_unknown": "Unknown command {}",
            },
            "enable_eeprom": True,
            "support_M503": True,
            "resend_ratio": 0,
            "locked": False,
            "passcode": "1234",
        }

    def get_settings_version(self):
        # self._settings.clean_all_data()
        return 1

    def virtual_printer_factory(self, comm_instance, port, baudrate, read_timeout):
        if not port == self.PORT_NAME:
            return None

        if not self.enabled:
            return None

        import logging.handlers

        from octoprint.logging.handlers import CleaningTimedRotatingFileHandler

        seriallog_handler = CleaningTimedRotatingFileHandler(
            self._settings.get_plugin_logfile_path(postfix="serial"),
            when="D",
            backupCount=3,
        )
        seriallog_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        seriallog_handler.setLevel(logging.DEBUG)

        from . import virtual

        serial_obj = virtual.VirtualPrinter(
            self._settings,
            data_folder=self.get_plugin_data_folder(),
            seriallog_handler=seriallog_handler,
            read_timeout=float(read_timeout),
            faked_baudrate=baudrate,
        )
        return serial_obj

    def get_additional_port_names(self, *args, **kwargs):
        if self.enabled:
            return [self.PORT_NAME]
        else:
            return []
