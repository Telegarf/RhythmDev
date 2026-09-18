from dataclasses import dataclass, field, asdict
from pathlib import Path
from uuid import UUID, uuid4
from Scripts.Utilities.Savers import Saver, launcher_saver
import subprocess

@dataclass
class SavingData:
    name:str
    uuid : UUID = field(default_factory=lambda: str(uuid4()), kw_only=True)

    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


    
@dataclass
class Project(SavingData):
    project_path: str
    project_id: str

    def get_backup_name(self):
        return f"{self.name.lower()}_backup"



@dataclass
class Command(SavingData):
    alias: str

    def get_path(self):
        commands_dir = Path("commands")
        commands_dir.mkdir(exist_ok=True)
        
        return commands_dir / f"{self.name}.ps1"
    
    def open_command(self):

        file_path = self.get_path()

        if not file_path.exists():
            file_path.touch()

        subprocess.Popen([r"D:\Microsoft VS Code\Code.exe", str(file_path)])

    def get_command_text(self):
        with open(self.get_path(), "r") as f:
            full_text = ""
            for line in f.readlines():
                full_text += line
        return full_text

@dataclass
class Launcher(SavingData):

    def get_file_path(self, saver: Saver) -> str:
        return Path(saver.get_property("cmd_command_path")) / f"{self.name}.cmd"