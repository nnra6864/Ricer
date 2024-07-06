import os, re
from colorama import Fore
from Color import Color

class File:
    def __init__(self, name, path, target_path, format):
        self.name = name
        self.path = path
        self.target_path = target_path
        self.format = format
        self.dirname = os.path.dirname(self.path)
        self.target_dirname = os.path.dirname(self.target_path)

    def write_file(self):
        from Config import Config
        print(f"{Fore.GREEN}\n\nUpdating {Fore.BLUE}{self.target_path}\n")
        
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

        if not os.path.isdir(self.target_dirname):
            print(f"{Fore.BLUE}{self.target_dirname} {Fore.YELLOW}doesn't exist, creating now")
            Config.create_dir(self.target_dirname)


        with open(self.target_path, 'w') as target:
            print()

    def edit_template(self) -> str:
        from Config import Config

        with open(self.path, 'r') as template:
            content = template.read()

        ricer_col_pattern = re.compile(r'\bricer\.col\.\w+(?:\.\w+)*\(?.*?\)?\b')
        matches = ricer_col_pattern.finditer(content)

        for match in matches:
            color = self.read_color(match)
        return ""

    def read_color(self, match) -> Color:
        from Config import Config

        col_name = match.group(1)
        if not col_name in Config.colors:
            raise KeyError(f"{Fore.RED}Color {Fore.BLUE}{col_name} {Fore.RED}is not defined in {Fore.BLUE}{Config.cfg_path}")
        col = Config.colors.get(col_name)

        col_format = match.group(2)
        if col_format is None:
            col_format = self.format
        if not col_format in Config.color_formats:
            raise ValueError(
                f"{Fore.BLUE}{col_format} {Fore.RED}is not a valid color format\n"
                f"{Fore.BLUE}{self.path}"
            )
        form = col_format
        
        return col.format(form)
        
