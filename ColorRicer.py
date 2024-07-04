from Color import Color
import os, toml, shutil

class File:
    def __init__(self, name, path, format):
        self.name = name
        self.path = path
        self.format = format

formats = { "hex", "rgb", "rgb01" }
alpha_formats = { "hexa", "rgba", "rgba01" }
channels = { "r", "g", "b" }
alpha_channels = { "r", "g", "b", "a" }

extended_formats = {f"{base}.{chan}" for base in formats for chan in channels}
extended_alpha_formats = {f"{base}.{chan}" for base in alpha_formats for chan in alpha_channels}
valid_formats = formats | extended_formats | alpha_formats | extended_alpha_formats

def is_valid_format(form):
    return form in valid_formats

format = "hex"
colors = []
files = []

def load_config():
    global format, colors, files
    cfg_path = os.path.expanduser("~/.config/ColorRicer.toml")

    if not os.path.exists(cfg_path):
        template = os.path.join(os.path.dirname(__file__), "ColorRicer.toml")
        if not os.path.exists(template):
            raise FileNotFoundError("ColorRicer.toml is missing from the script directory, get the new one here: https://github.com/nnra6864/ColorRicer/blob/master/ColorRicer.toml")
        shutil.copy(template, cfg_path)

    with open(cfg_path, 'r') as cfg:
        config = toml.load(cfg)

    if "format" in config:
        format = config["format"]
        if not is_valid_format(format):
            raise ValueError(f"Format is not valid: {format}")

    if "Colors" in config:
        cfg_colors = config["Colors"]
        for name, col in cfg_colors.items():
            colors.append(Color(name, str(col)))

    if "Files" in config:
        cfg_files = config["Files"]
        for name, file in cfg_files.items():
            if isinstance(file, str):
                files.append(File(name, file, format))

            elif isinstance(file, list) and len(file) in [1, 2]:
                form = format if len(file) == 1 else file[1]
                if not is_valid_format(form):
                    raise ValueError(f"Invalid format: {form} for file: {name}")
                files.append(File(name, os.path.expanduser(file[0]), form))

            else:
                raise ValueError(f"Invalid config file entry: {name} = {file}")

load_config()

print(f"Default Format: {format}")

for col in colors:
    print(f"Name: {col.name} | HEXA: {col.hexa} | RGBA: {col.rgba} | RGBA01: {col.rgba01}")

for file in files:
    print(f"Name: {file.name} | Format: {file.format} | Path: {file.path}")
