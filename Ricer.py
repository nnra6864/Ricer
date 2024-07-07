import os, sys

from colorama import Fore, init
init(autoreset=True) #Should be done before importing other modules

from Color import Color
from File import File
from Config import Config

cfg_path = sys.argv[1] if len(sys.argv) > 1 else "~/.config/Ricer/Config.toml"
Config.init(cfg_path)
for name, file in Config.files.items():
    file.rice()
