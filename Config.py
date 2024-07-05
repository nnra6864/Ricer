import os, toml, shutil, glob, requests
from colorama import Fore

class Config:
    _initialized = False

    default_format = "{hex}"
    color_log_format = "Name: {name} | HEXA: {hexa} | RGBA: {rgba} | RGBA01: {rgba01}"
    file_log_format = "Name: {name}\nPath: {path}\nTarget Path: {target_path}\nFormat: {format}\n"
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
        #Following modules have to be imported here to avoid circular imports
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
        
        print(f"{Fore.GREEN}\n\nLoading config\n")

        with open(cfg_path, 'r') as cfg:
            config = toml.load(cfg)

        if "default_format" in config:
            cls.default_format = config["default_format"]
            print(f"{Fore.GREEN}Loaded{Fore.RESET} default format: {Fore.BLUE + cls.default_format}")
    
        if "color_log_format" in config:
            cls.color_log_format = config["color_log_format"]
            print(f"{Fore.GREEN}Loaded{Fore.RESET} color_log_format: {Fore.BLUE + cls.color_log_format}")

        if "file_log_format" in config:
            cls.file_log_format = config["file_log_format"]
            print(f"{Fore.GREEN}Loaded{Fore.RESET} file_log_format: {Fore.BLUE + cls.file_log_format}")

        if "rgba01_precision" in config:
            precision = str(config["rgba01_precision"])
            if not precision.isdigit():
                raise ValueError(f"{Fore.RED}rgba01_precision must be a positive integer: {precision}")
            cls.rgba01_precision = int(precision)
    
        if "Colors" in config:
            print(f"{Fore.GREEN}\n\nLoading Colors\n")
            cfg_colors = config["Colors"]
            for name, color in cfg_colors.items():
                col = Color(name, str(color))
                cls.colors.append(col)
                print(cls.color_log_format.format(name = f"{Fore.BLUE}{col.name}{Fore.RESET}", hexa = f"{Fore.BLUE}{col.hexa}{Fore.RESET}", rgba = f"{Fore.BLUE}{col.rgba}{Fore.RESET}", rgba01 = f"{Fore.BLUE}{col.rgba01}{Fore.RESET}"))
    
        if "Files" in config:
            print(f"{Fore.GREEN}\n\nLoading Files\n")
            cfg_files = config["Files"]
            for name, file_data in cfg_files.items():
                path = f"{os.path.join(files_dir, name)}*"
                target_path = ""
                format = Config.default_format

                if isinstance(file_data, str):
                    target_path = os.path.expanduser(file_data)

                elif isinstance(file_data, list) and len(file_data) in [1, 2]:
                    target_path = os.path.expanduser(file_data[0])
                    if len(file_data) == 2: format = file_data[1]
                else:
                    raise ValueError(f"{Fore.RED}Invalid file entry: {Fore.BLUE}{name}{Fore.RED} = {Fore.BLUE}\"{file_data}\"{Fore.RESET}")
                
                files = glob.glob(path)
                if len(files) == 0:
                    raise ValueError(f"{Fore.RED}File with the name {Fore.BLUE}{name}{Fore.RED} doesn't exist in {Fore.BLUE}{files_dir}{Fore.RESET}")
                path = files[0]
                file = File(name, path, target_path, format)
                cls.files.append(file)
                print(cls.file_log_format.format(name = f"{Fore.BLUE}{file.name}{Fore.RESET}", path = f"{Fore.BLUE}{file.path}{Fore.RESET}", target_path = f"{Fore.BLUE}{file.target_path}{Fore.RESET}", format = f"{Fore.BLUE}{file.format}{Fore.RESET}"))

