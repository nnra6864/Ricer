import os, toml, shutil, requests
from colorama import Fore
from Color import Color
from File import File

class Config:
    _initialized = False

    default_format = "{hex}"
    color_log_format = "Name: {name} | HEXA: {hexa} | RGBA: {rgba} | RGBA01: {rgba01}"
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
        print(f"{Fore.YELLOW}{dir} doesn't exist")
        print(f"Creating {Fore.BLUE+dir}")
        try:
            os.makedirs(dir)
            print(f"{Fore.GREEN}{dir} created successfully")
        except OSError as err:
            raise OSError(f"{Fore.RED}{err}")

    @staticmethod
    def download_file(url, save_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"{Fore.GREEN}Downloaded {url} to {save_path}")
        else:
            raise Exception(f"{Fore.RED}Failed to download {url}: {response}")

    @classmethod
    def load_config(cls):
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
                    raise Exception(f"{ex}\n{Fore.RESET}Try manually downloading the file and placing it in the same dir as ColorRicer\nTemplate: {Fore.BLUE}{template_link}{Fore.RESET}\nColorRicer: {Fore.BLUE}") from None

            print(f"Moving {Fore.BLUE}{template}{Fore.RESET} to {Fore.BLUE}{cfg_path}")
            shutil.copy(template, cfg_path)
            print(Fore.GREEN + "Copied ColorRicer.toml to ~/.config/ColorRicer.toml")
        
        else:
            print(Fore.GREEN + "Found config at ~/.config/ColorRicer.toml")

        print("Loading config\n")

        with open(cfg_path, 'r') as cfg:
            config = toml.load(cfg)

        if "default_format" in config:
            cls.default_format = config["default_format"]
            print(f"Loaded default format: {Fore.BLUE + cls.default_format}")
    
        if "color_log_format" in config:
            cls.color_log_format = config["color_log_format"]
            print(f"Loaded color_log_format: {Fore.BLUE + cls.color_log_format}")
    
        if "Colors" in config:
            print("\nLoading Colors")
            cfg_colors = config["Colors"]
            for name, col in cfg_colors.items():
                cls.colors.append(Color(name, str(col)))
                print(cls.color_log_format.format(name = col.name, hexa = col.hexa, rgba = col.rgba, rgba01 = col.rgba01))
    
        if "Files" in config:
            cfg_files = config["Files"]
            for name, file in cfg_files.items():
                if isinstance(file, str):
                    cls.files.append(File(name, file, Config.format))
    
                elif isinstance(file, list) and len(file) in [1, 2]:
                    form = cls.default_format if len(file) == 1 else file[1]
                    cls.files.append(File(name, os.path.expanduser(file[0]), form))
    
                else:
                    raise ValueError(f"Invalid config file entry: {name} = {file}")
