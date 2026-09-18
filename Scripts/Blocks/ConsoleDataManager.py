from pathlib import Path
from Scripts.SavingData import Project
import Scripts.Savers as Savers
import subprocess

class ConsoleDataManager:
    def __init__(self, saver:Savers):
        self.saver = saver

    def select_project(self, project:Project):
        self.change_file("id", project.project_id)  
        self.change_file("name", project.name)  
        self.change_file("path", project.project_path)  

        self.saver.set_current_project(project)
    def change_file(self, name:str, text:str):

        if not name.startswith("current_project_"):
            name = f"current_project_{name}"

        path = Path("WindowsVariables") / f"{name}.txt"

        with open(path, "w") as f:
            f.write(text)

    def install_environment_variables(self):
        for name in (
            "PRJ_NAME",
            "PRJ_PATH",
            "PRJ_ID",
        ):
            subprocess.run(["setx", name, ""], check=True)
    def set_current_project(self, project:Project):
        data = self.saver.get_data()
        data["currentProject"] = project.uuid

        self.saver.save(data)

    def save_to_profile(self):
        alies:str = ""
        commands:str = ""
        with open(Path("commands") / "__def__.ps1", "r") as f:
            start = ""
            for line in f.readlines():
                start += line

        for command in self.Commands.get_items():
            commands += f"{command.get_command_text()} \n"
            alies += f"Set-Alias -Name {command.alias} -Value {command.name} -Force \n"
    
        result:str = f"{start} \n\n\n {commands} \n\n{alies}"
    
        profile = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "$PROFILE"],
            text=True
        ).strip()
    
        with Path(profile).open("w", encoding="utf-8") as f:
            f.write(result)