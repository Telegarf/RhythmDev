from config import Config
from pathlib import Path
from Scripts.Utilities.SavingData import Project, Command
from Scripts.Utilities.Savers import project_saver, command_saver
from Scripts.Utilities.Repositories import FileRepository
import subprocess

def select_project(project:Project):
    change_file("id", project.project_id)  
    change_file("name", project.name)  
    change_file("path", project.project_path)  

    project_saver.set_property("currentProject", project.uuid)

def change_file(name:str, text:str):

    if not name.startswith("current_project_"):
        name = f"current_project_{name}"

    path = get_variables_dir()
    path.mkdir(exist_ok=True)
    path = path / f"{name}.txt"
    with open(path, "w") as f:
        f.write(text)

def set_environment_variable(var:str, value:str):
    subprocess.run(["setx", var, value], check=True)

def save_to_profile():
    alies:str = ""
    commands:str = ""

    with open(Path("default_data") / "__def__.ps1", "r") as f:
        commands = ""
        for line in f.readlines():
            commands += line
        commands += "\n\n\n"
    repo:FileRepository = command_saver.reps[Command]
    for command in repo.get_items():
        commands += f"{repo.get_file_text(command)} \n"
        alies += f"Set-Alias -Name {command.alias} -Value {command.name} -Force \n"

    result:str = f"{commands} \n\n{alies}"

    profile = subprocess.check_output(
        ["powershell", "-NoProfile", "-Command", "$PROFILE"],
        text=True
    ).strip()

    with Path(profile).open("w", encoding="utf-8") as f:
        f.write(result)

def get_variables_dir() -> Path:
    return Path(Config.get_property("storage_dir_path"))/ "WindowsVariables"