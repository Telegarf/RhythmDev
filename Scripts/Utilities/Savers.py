from pathlib import Path
from Scripts.Utilities.SavingData import *
import subprocess
import json
from Scripts.Utilities.Repositories import Repository



class BlockSaver:
    def __init__(self, file_name:str):
        file_path = Path(file_name)

        if file_path.suffix != ".json":
            file_path = file_path.with_suffix(".json")

        path = Path(get_storage_dir()) / file_path
        path.parent.mkdir(exist_ok=True, parents=True)

        self.path = path
        self.reps = {}

    def get_data(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    def save(self, dataToSave):
        with open(self.path, "w") as f:
            json.dump(dataToSave, f, indent=4)
    def clear(self):
        data = {}
        self.save(data)
        
    def get_property(self, tag:str):
        data = self.get_data()

        return data.get(tag) or ""
    def set_property(self, tag:str, path:str):
        data = self.get_data()

        data[tag] = path

        self.save(data)

    def add_repository(self, data_type: type, rep: Repository[SavingData]):
        if rep.saver is not None:
            raise ValueError("Repository already belongs to a Saver")
        if data_type in self.reps:
            raise ValueError(f"Repository for {data_type.__name__} already exists")
        
        rep.saver = self
        self.reps[data_type] = rep

main_saver = Saver("data.json")

def get_storage_dir():
    return main_saver.get_property("main_dir_path")









command_saver = BlockSaver("commands.json")
project_saver = BlockSaver("projects.json")
launcher_saver = BlockSaver("launcher.json")

#Command
def on_command_added(command: Command):
    command.get_path().touch()
    with open(command.get_path(), "w") as f:
        text = f"function {command.name}" + r" {" + "\n \n}"
        f.writelines(text)
com_rep = Repository("commands", Command)
command_saver.add_repository(Command, com_rep)
com_rep.add_callback(com_rep.Commands.add_item, on_command_added)

#Project
prj_rep = Repository("projects", Project)
project_saver.add_repository(Project, prj_rep)

#Cmd Command
lch_rep = Repository("launchers", Launcher)
launcher_saver.add_repository(lch_rep)











"""
        self.Projects = Repository(self, "projects", Project)

        self.Commands = Repository(self, "commands", Command)
        self.Commands.add_callback(
            self.Commands.add_item, 
            self.on_command_added
        )
        
    def on_command_added(self, command: Command):
        command.get_path().touch()
        with open(command.get_path(), "w") as f:
            text = f"function {command.name}" + r" {" + "\n \n}"
            f.writelines(text)
"""