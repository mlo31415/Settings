from __future__ import annotations
from typing import Any

import os
import json

class Settings():
    g_settings:dict[str, Any]={}
    g_settingsFilename: str=""

    def Save(self) -> None:
        if len(Settings.g_settingsFilename) > 0:
            with open(Settings.g_settingsFilename, "w+") as file:
                file.write(json.dumps(Settings.g_settings))

    def Load(self, fname: str) -> None:
        Settings.g_settingsFilename=os.path.join(os.getcwd(), fname)
        if os.path.exists(fname):
            with open(fname, "r") as file:
                lines=file.read()
                if len(lines) > 0:
                    Settings.g_settings=json.loads(lines)

    def Put(self, name: str, val: Any) -> None:
        Settings.g_settings[name]=val
        self.Save()

    def Get(self, name: str, default: Any=None) -> Any:
        if name not in Settings.g_settings.keys():
            return default
        return Settings.g_settings[name]