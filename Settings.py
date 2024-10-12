from typing import Any

import os
import json

from HelpersPackage import MessageBox, ReadListAsParmDict, MessageLog

class Settings:
    # A dictionary of named dictionaries (plus the default unnamed dictionary)
    # Each name returns a string and a dict.
    #   The string is the dict's source pathname
    #   The dict is the dictionary of parameters loaded from it.
    #   Dicts are accessed case-insensitive
    g_dicts: dict[str, tuple[str, dict[str, Any]]]={}
    g_dictname: str=""

    def __init__(self, fname: str=""):
        #print(f"Settings({fname=})")
        Settings.g_dictname=fname       # This is the name of the dictionary to be used.
        if fname not in Settings.g_dicts:
            Settings.g_dicts[fname]=("", {})        # If a new dictionary has been requested, create it.

    @property
    def Dict(self) -> dict[str, Any]:
        # Use g_dictname (the value passed in by  Settings("xxx") to choose the dictionary to be returned
        return Settings.g_dicts[Settings.g_dictname][1]
    @Dict.setter
    def Dict(self, val: dict[str, Any]):
        d=Settings.g_dicts[Settings.g_dictname]
        Settings.g_dicts[Settings.g_dictname]=(d[0], val)

    @property
    def Dictpath(self) -> str:
        # Use g_dictname (the value passed in by  Settings("xxx") to choose the dictionary to be returned
        return Settings.g_dicts[Settings.g_dictname][0]
    @Dictpath.setter
    def Dictpath(self, val: str):
        d=Settings.g_dicts[Settings.g_dictname]
        Settings.g_dicts[Settings.g_dictname]=(val, d[1])

    def Save(self) -> None:
        if len(self.Dictpath) > 0:
            with open(self.Dictpath, "w+") as file:
                if os.path.splitext(self.Dictpath)[1].lower() == ".txt":
                    lst="\n".join([f"{x}={y}" for x, y in self.Dict.items()])
                    file.write(lst)
                elif os.path.splitext(self.Dictpath)[1].lower() == ".json":
                    file.write(json.dumps(self.Dict))
                else:
                    MessageBox(f"Can't save. Settings file '{self.Dictpath}' has an extension other than 'txt' or 'json'", ignoredebugger=True)

    # Load a settings file.  It can be either .json or .txt (the latter being a list of names followed '=' followed by values)
    def Load(self, pathname: str, MustExist: bool=False, SuppressMessageBox: bool=False) -> bool:
        if MustExist and not os.path.exists(pathname):
            if not SuppressMessageBox:
                MessageBox(f"Settings file '{pathname}' is missing.  This is unlikely to end well...", ignoredebugger=True)
            return False

        if os.path.splitext(pathname)[1].lower() == ".txt":
            assert True     # TODO: Need to reconcile ParmDict with Dict
            self.Dict=ReadListAsParmDict(pathname, isFatal=True)
            if self.Dict is None or len(self.Dict) == 0:
                MessageLog(f"Can't open/read {pathname}")
                exit(999)
            self.Dictpath=os.path.join(os.getcwd(), pathname)
            return True

        # OK, either the settings file exists or we don't care if it exists or not.
        # (If it doesn't exist, it will be created on save.)
        #print(f"{pathname=} exists? {os.path.exists(pathname)}")
        with open(pathname, "r") as file:
            lines=file.read()
            if len(lines) > 0:
                self.Dict=json.loads(lines)
        self.Dictpath=os.path.join(os.getcwd(), pathname)
        return True


    def Put(self, name: str, val: Any) -> None:
        self.Dict[name]=val
        #print(f"Put({self.g_dictname}) {name}={val}")
        self.Save()

    # Get a parameter from the settings dictionary
    # Names are matched case-insensitive
    def Get(self, name: str, default: Any=None) -> Any:
        keys=[x for x in self.Dict.keys()]
        kikeys=[x.casefold() for x in self.Dict.keys()]
        name=name.casefold()
        if name not in kikeys:
            return default
        loc=kikeys.index(name)
        #print(f"Get({self.g_dictname}) {name}={self.Dict[name]}")
        return self.Dict[keys[loc]]

    # Return True if Name exists and is (case-inseneitive) Yes or True
    def IsTrue(self, name: str, default: bool=False) -> bool:
        ret=self.Get(name, default).lower()
        if isinstance(ret, bool):
            return ret
        return ret == "true" or ret == "yes"


    # Dump out the settings as dict pairs
    def Dump(self) -> str:
        s=""
        for key, val in self.Dict.items():
            s+=f"'{key}': '{val}'\n"
        return s
