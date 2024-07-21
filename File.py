import os, re
from colorama import Fore

class File:
    def __init__(self, name, path, target_path, color_format):
        self.name = name
        self.path = path
        self.target_path = target_path
        self.color_format = color_format
        self.dirname = os.path.dirname(self.path)
        self.target_dirname = os.path.dirname(self.target_path)

    def rice(self):
        from Config import Config
        print(f"{Fore.GREEN}\nRicing {Fore.BLUE}{self.name}")
        
        if os.path.exists(self.target_path):
            print(f"{Fore.BLUE}{os.path.basename(self.target_path)} {Fore.YELLOW}already exists at {Fore.BLUE}{self.target_dirname}")
            if Config.replace_files:
                os.remove(self.target_path)
                print(f"{Fore.GREEN}Removed {Fore.BLUE}{self.target_path}")
            else:
                backup_count = 0
                backup_path = f"{self.target_path}.backup"
                while os.path.exists(backup_path):
                    backup_count += 1
                    backup_path = f"{self.target_path}.backup{backup_count}"
                os.rename(self.target_path, backup_path)
                print(f"{Fore.GREEN}Backed up to {Fore.BLUE}{backup_path}")

        if not os.path.isdir(self.target_dirname):
            print(f"{Fore.BLUE}{self.target_dirname} {Fore.YELLOW}doesn't exist, creating now")
            Config.create_dir(self.target_dirname)

        with open(self.target_path, 'w') as target_file:
            target_file.write(self.rice_template())

    def rice_template(self) -> str:
        from Config import Config
        with open(self.path, 'r') as template:
            print(f"Reading {Fore.BLUE}{self.path}")
            content = template.read()
        
        alias = Config.alias
        ricer_val_pattern = re.compile(fr'{re.escape(alias)}\.val\.(\w+)([\\ ]?)')
        ricer_col_pattern = re.compile(fr'{re.escape(alias)}\.col\.(\w+)(?:\.(\w+))?(?:\((.*?)\))?', re.DOTALL)
        
        content = ricer_val_pattern.sub(lambda match: self.get_value(match) + (match.group(2) if match.group(2) != '\\' else ''), content)
        content = ricer_col_pattern.sub(self.get_color, content)
        return content
    
    def get_value(self, match) -> str:
        from Config import Config
        val = match.group(1)
        if not val in Config.values:
            raise KeyError(f"{Fore.RED}Value {Fore.BLUE}{val} {Fore.RED}is not defined in {Fore.BLUE}{Config.cfg_path}")
        value = Config.values[val]
        print(f"Replaced {Fore.BLUE}{match.group(0)} {Fore.RESET}with {Fore.BLUE}{value}")
        return str(value)

    def get_color(self, match) -> str:
        from Config import Config
        
        col_name = match.group(1)
        if not col_name in Config.colors:
            raise KeyError(f"{Fore.RED}Color {Fore.BLUE}{col_name} {Fore.RED}is not defined in {Fore.BLUE}{Config.cfg_path}")
        col = Config.colors[col_name]

        col_format = match.group(2)
        if col_format is None:
            col_format = self.color_format
        if not col_format in Config.color_formats:
            raise ValueError(
                f"{Fore.BLUE}{col_format} {Fore.RED}is not a valid color format\n"
                f"{Fore.BLUE}{self.path}"
            )
        form = col_format

        if form == "format":
            col_format = match.group(3)
            if not col_format is None:
                form = col_format

        color = col.format_color(form)
        print(f"Replaced {Fore.BLUE}{match.group(0)} {Fore.RESET}with {Fore.BLUE}{color}")
        return color
        
