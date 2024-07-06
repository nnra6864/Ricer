import os
from colorama import Fore


class File:
    def __init__(self, name, path, target_path, format):
        self.name = name
        self.path = path
        self.target_path = target_path
        self.format = format

    def write_file(self):
        print(f"{Fore.GREEN}\n\nWriting config files\n")
        #TODO: Implement a check if the file exists
        if os.path.exists(self.target_path):
            print(f"{Fore.BLUE}{os.path.basename(self.target_path)} {Fore.YELLOW}already exists at {Fore.BLUE}{os.path.dirname(self.target_path)}")

        #with open(path, )
