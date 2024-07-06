import os, toml, shutil, glob, requests
from colorama import Fore
from typing import Union, List
from Color import Color
from File import File

class Config:
    _initialized = False
    cfg_path = ""
    cfg_dir = ""
    files_path = ""
    default_format = "hex"
    color_log_format = "Name: {name} | HEXA: {hexa} | RGBA: {rgba} | RGBA01: {rgba01}"
    file_log_format = "Name: {name}\nPath: {path}\nTarget Path: {target_path}\nFormat: {format}\n"
    rgba01_precision = 2
    replace_files = False
    values = {}
    colors = {}
    files = {}

    color_formats = ("hex", "hexa", "hr", "hg", "hb", "ha",
                     "rgb", "rgba", "r", "g", "b", "a",
                     "rgb01", "rgba01", "r01", "g01", "b01", "a01",
                     "format")

    @classmethod
    def init(cls, cfg_path):
        if cls._initialized:
            return
        cls.load_config(cfg_path)
        cls._initialized = True

    @classmethod
    def load_config(cls, cfg_path):
        Config.cfg_path = cfg_path
        Config.cfg_dir = os.path.dirname(cfg_path)
        Config.files_dir = Config.cfg_dir+"/Files/"
        
        if not os.path.exists(Config.cfg_dir):
            Config.create_dir(Config.cfg_dir)
            print("")

        if not os.path.exists(Config.files_dir):
            Config.create_dir(Config.files_dir)
            print("")

        if not os.path.exists(cfg_path):
            print(f"{Fore.YELLOW}Config not found")
            template = os.path.join(os.path.dirname(__file__), "Config.toml")

            if not os.path.exists(template):
                print(f"{Fore.YELLOW}Config template not found")
                print(f"Downloading config template from GitHub")
                template_link = "https://github.com/nnra6864/ColorRicer/blob/master/Config.toml"
                raw_template_link = "https://raw.githubusercontent.com/nnra6864/ColorRicer/master/Config.toml"
                try:
                    Config.download_file(raw_template_link, template)
                except Exception as ex:
                    raise Exception(
                        f"{ex}\n"
                        f"Try manually downloading the file and placing it in the same dir as ColorRicer\n"
                        f"Template: {Fore.BLUE}{template_link}{Fore.RESET}\n"
                        f"ColorRicer: {Fore.BLUE}{cfg_path}"
                    ) from None

            print(f"Copying {Fore.BLUE}{template}{Fore.RESET} to {Fore.BLUE}{cfg_path}")
            shutil.copy(template, cfg_path)
            print(f"{Fore.GREEN}Copied {Fore.BLUE}{template}{Fore.GREEN} to {Fore.BLUE}{cfg_path}")
        
        else:
            print(f"{Fore.GREEN}Found config at {Fore.BLUE}{cfg_path}")
        
        print(f"{Fore.GREEN}\nLoading config")

        with open(cfg_path, 'r') as cfg:
            config = toml.load(cfg)

        if "default_format" in config:
            default_format = config["default_format"]
            if not isinstance(default_format, str):
                raise ValueError(f"{Fore.RED}default_format must be a string: {default_format}{Fore.RESET}")
            Config.default_format = default_format
            print(f"{Fore.GREEN}Loaded{Fore.RESET} default format: {Fore.BLUE}{cls.default_format}")
    
        if "color_log_format" in config:
            color_log_format = config["color_log_format"]
            if not isinstance(color_log_format, str):
                raise ValueError(f"{Fore.RED}color_log_format must be a string: {color_log_format}{Fore.RESET}")
            Config.color_log_format = color_log_format
            print(f"{Fore.GREEN}Loaded{Fore.RESET} color_log_format: {Fore.BLUE}{cls.color_log_format}")

        if "file_log_format" in config:
            file_log_format = config["file_log_format"]
            if not isinstance(file_log_format, str):
                raise ValueError(f"{Fore.RED}file_log_format must be a string: {file_log_format}{Fore.RESET}")
            Config.file_log_format = file_log_format
            print(f"{Fore.GREEN}Loaded{Fore.RESET} file_log_format: {Fore.BLUE}{Config.file_log_format}")

        if "rgba01_precision" in config:
            rgba01_precision = config["rgba01_precision"]
            if not isinstance(rgba01_precision, int) and rgba01_precision < 1:
                raise ValueError(f"{Fore.RED}rgba01_precision must be a positive integer: {rgba01_precision}{Fore.RESET}")
            Config.rgba01_precision = int(rgba01_precision)
            print(f"{Fore.GREEN}Loaded{Fore.RESET} rgba01_precision: {Fore.BLUE}{Config.rgba01_precision}")
        
        if "replace_files" in config:
            replace_files = config["replace_files"]
            if not isinstance(replace_files, bool):
                raise ValueError(f"{Fore.RED}replace_files must be a bool: {replace_files}{Fore.RESET}")
            Config.replace_files = replace_files
            print(f"{Fore.GREEN}Loaded{Fore.RESET} replace_files: {Fore.BLUE}{Config.replace_files}")


        if "Values" in config:
            print(f"{Fore.GREEN}\nLoading Values")
            cfg_values = config["Values"]
            for name, data in cfg_values.items():
                Config.values[name] = data
                print(f"{name}: {Fore.BLUE}{data}")

        if "Colors" in config:
            print(f"{Fore.GREEN}\nLoading Colors")
            cfg_colors = config["Colors"]
            for name, data in cfg_colors.items():
                Config.colors[name] = (Config.load_color(name, data))
    
        if "Files" in config:
            print(f"{Fore.GREEN}\nLoading Files")
            cfg_files = config["Files"]
            for name, data in cfg_files.items():
                Config.files[name] = (Config.load_file(name, data))
    
    
    @staticmethod
    def create_dir(dir):
        print(f"{Fore.BLUE}{dir} {Fore.YELLOW}doesn't exist")
        print(f"Creating {Fore.BLUE}{dir}")
        try:
            os.makedirs(dir, exist_ok=True)
            print(f"{Fore.BLUE}{dir} {Fore.GREEN}created successfully")
        except OSError as err:
            raise OSError(f"{Fore.RED}{err}{Fore.RESET}")
    
    @staticmethod
    def download_file(url, save_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"{Fore.GREEN}Downloaded {Fore.BLUE}{url}{Fore.GREEN} to {Fore.BLUE}{save_path}")
        else:
            raise Exception(f"{Fore.RED}Failed to download {Fore.BLUE}{url}{Fore.RED}: {response}{Fore.RESET}")

    @staticmethod
    def load_color(name: str, data: str) -> Color:
        color = Color(name, str(data))
        print(Config.color_log_format.format(
            name = f"{Fore.BLUE}{color.name}{Fore.RESET}",
            hexa = f"{Fore.BLUE}{color.hexa}{Fore.RESET}",
            rgba = f"{Fore.BLUE}{color.rgba}{Fore.RESET}",
            rgba01 = f"{Fore.BLUE}{color.rgba01}{Fore.RESET}"
        ))
        return color

    @staticmethod
    def load_file(name: str, file_data: Union[str, List[str]]) -> File:
        path = f"{os.path.join(Config.files_dir, name)}*"
        target_path = ""
        format = Config.default_format

        if isinstance(file_data, str):
            target_path = os.path.expanduser(file_data)

        elif isinstance(file_data, list) and len(file_data) in [1, 2]:
            target_path = os.path.expanduser(file_data[0])
            if len(file_data) == 2: format = file_data[1]
        else:
            raise ValueError(
                f"{Fore.RED}Invalid file entry:\n",
                f"{Fore.BLUE}{name}{Fore.RED} = {Fore.BLUE}\"{file_data}\"{Fore.RESET}"
            )
        
        files = glob.glob(path)
        if len(files) == 0:
            raise ValueError(
                f"{Fore.RED}File with the name {Fore.BLUE}{name}{Fore.RED} doesn't exist in:\n",
                f"{Fore.BLUE}{Config.files_dir}{Fore.RESET}"
            )
        if os.path.isdir(target_path):
            raise ValueError(
                f"{Fore.RED}Target path must be a file, not a directory:\n",
                f"{Fore.BLUE}{name} {Fore.RESET}= {Fore.BLUE}\"{file_data}\"{Fore.RESET}"
            )

        path = files[0]
        file = File(name, path, target_path, format)
        print(Config.file_log_format.format(
            name = f"{Fore.BLUE}{file.name}{Fore.RESET}",
            path = f"{Fore.BLUE}{file.path}{Fore.RESET}",
            target_path = f"{Fore.BLUE}{file.target_path}{Fore.RESET}",
            format = f"{Fore.BLUE}{file.format}{Fore.RESET}"
        ))
        return file

