from pathlib import Path
from Scripts.Utilities.SavingData import *
import json
from Scripts.Utilities.Repositories import ObjectRepository, FileRepository
from config import Config

class BlockSaver:
    def __init__(self, file_name:str, path_to_file="/"):
        if(path_to_file == "/"):
            path_to_file = Config.get_property("storage_dir_path")
        file_path = Path(file_name)

        if file_path.suffix != ".json":
            file_path = file_path.with_suffix(".json")

        path = Path(path_to_file) / "saves" / file_path
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch()

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

    def add_repository(self, data_type: type, rep: ObjectRepository[SavingData]):
        if rep.saver is not None:
            raise ValueError("Repository already belongs to a Saver")
        if data_type in self.reps:
            raise ValueError(f"Repository for {data_type.__name__} already exists")
        
        rep.saver = self
        self.reps[data_type] = rep










command_saver = BlockSaver("commands.json")
project_saver = BlockSaver("projects.json")
launcher_saver = BlockSaver("launcher.json")


#Command
com_rep = FileRepository("_commands", "commands", Command)
command_saver.add_repository(Command, com_rep)

#Project
prj_rep = ObjectRepository("projects", Project)
project_saver.add_repository(Project, prj_rep)

#Launcher
lch_rep = FileRepository("_launchers", "launchers", Launcher)
launcher_saver.add_repository(Launcher, lch_rep)











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