import os, toml, shutil, requests
from colorama import Fore

class Config:
    _initialized = False

    default_format = "{hex}"
    color_log_format = "Name: {name} | HEXA: {hexa} | RGBA: {rgba} | RGBA01: {rgba01}"
    rgba01_precision = 2
    colors = []
    files = []

    @classmethod
    def init(cls):
        if cls._initialized:
            return
        cls.load_config()
        cls._initialized = True

    @staticmethod
    def create_dir(dir):
        print(f"{Fore.BLUE}{dir} {Fore.YELLOW}doesn't exist")
        print(f"Creating {Fore.BLUE}{dir}")
        try:
            os.makedirs(dir)
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


    @classmethod
    def load_config(cls):
        #Has to be done here to avoid circular import
        from Color import Color
        from File import File

        cfg_dir = os.path.expanduser("~/.config/ColorRicer/")
        files_dir = cfg_dir+"Files/"
        cfg_path = cfg_dir + "Config.toml"
        
        if not os.path.exists(cfg_dir):
            Config.create_dir(cfg_dir)
            print("")

        if not os.path.exists(files_dir):
            Config.create_dir(files_dir)
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
                    raise Exception(f"{ex}\nTry manually downloading the file and placing it in the same dir as ColorRicer\nTemplate: {Fore.BLUE}{template_link}{Fore.RESET}\nColorRicer: {Fore.BLUE}{cfg_path}") from None

            print(f"Copying {Fore.BLUE}{template}{Fore.RESET} to {Fore.BLUE}{cfg_path}")
            shutil.copy(template, cfg_path)
            print(f"{Fore.GREEN}Copied {Fore.BLUE}{template}{Fore.GREEN} to {Fore.BLUE}{cfg_path}")
        
        else:
            print(f"{Fore.GREEN}Found config at {Fore.BLUE}{cfg_path}")
        
        print("\nLoading config")

        with open(cfg_path, 'r') as cfg:
            config = toml.load(cfg)

        if "default_format" in config:
            cls.default_format = config["default_format"]
            print(f"{Fore.GREEN}Loaded{Fore.RESET} default format: {Fore.BLUE + cls.default_format}")
    
        if "color_log_format" in config:
            cls.color_log_format = config["color_log_format"]
            print(f"{Fore.GREEN}Loaded{Fore.RESET} color_log_format: {Fore.BLUE + cls.color_log_format}")

        if "rgba01_precision" in config:
            precision = str(config["rgba01_precision"])
            if not precision.isdigit():
                raise ValueError(f"{Fore.RED}rgba01_precision must be a positive integer: {precision}")
            cls.rgba01_precision = int(precision)
    
        if "Colors" in config:
            print("\nLoading Colors")
            cfg_colors = config["Colors"]
            for name, color in cfg_colors.items():
                col = Color(name, str(color))
                cls.colors.append(col)
                print(cls.color_log_format.format(name = f"{Fore.BLUE}{col.name}{Fore.RESET}", hexa = f"{Fore.BLUE}{col.hexa}{Fore.RESET}", rgba = f"{Fore.BLUE}{col.rgba}{Fore.RESET}", rgba01 = f"{Fore.BLUE}{col.rgba01}{Fore.RESET}"))
    
        if "Files" in config:
            cfg_files = config["Files"]
            for name, file in cfg_files.items():
                if isinstance(file, str):
                    cls.files.append(File(name, file, Config.default_format))
    
                elif isinstance(file, list) and len(file) in [1, 2]:
                    form = cls.default_format if len(file) == 1 else file[1]
                    cls.files.append(File(name, os.path.expanduser(file[0]), form))
    
                else:
                    raise ValueError(f"Invalid config file entry: {name} = {file}")
