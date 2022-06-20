from __future__ import annotations
from typing import Any

import os
import json

from HelpersPackage import MessageBox, ReadListAsParmDict, MessageLog

class Settings:
    g_settings:dict[str, Any]={}
    g_settingsFilename: str=""

    def Save(self) -> None:
        if len(Settings.g_settingsFilename) > 0:
            with open(Settings.g_settingsFilename, "w+") as file:
                file.write(json.dumps(Settings.g_settings))

    def Load(self, fname: str, MustExist: bool=False) -> bool:
        if MustExist and not os.path.exists(fname):
            MessageBox(f"Settings file {fname} is missing.  This is unlikely to end well...", ignoredebugger=True)
            return False

        if os.path.splitext(fname)[1].lower() == ".txt":
            Settings.g_settings=ReadListAsParmDict(fname, isFatal=True)
            if Settings.g_settings is None or len(Settings.g_settings) == 0:
                MessageLog(f"Can't open/read {os.getcwd()}/parameters.txt")
                exit(999)
            Settings.g_settingsFilename=os.path.join(os.getcwd(), fname)
            return True

        # OK, with the settings file exists or we don't care if it exists or not.
        # (If it doesn't exist, it will be created on save.)
        with open(fname, "r") as file:
            lines=file.read()
            if len(lines) > 0:
                Settings.g_settings=json.loads(lines)
        Settings.g_settingsFilename=os.path.join(os.getcwd(), fname)
        return True



    def Put(self, name: str, val: Any) -> None:
        Settings.g_settings[name]=val
        self.Save()

    def Get(self, name: str, default: Any=None) -> Any:
        if name not in Settings.g_settings.keys():
            return default
        return Settings.g_settings[name]

    # Dump out the settings as dict pairs
    def Dump(self) -> str:
        s=""
        for key, val in self.g_settings.items():
            s+=f"'{key}': '{val}'\n"
        return s
