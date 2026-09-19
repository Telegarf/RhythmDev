from dataclasses import dataclass, field, asdict
from pathlib import Path
from uuid import UUID, uuid4

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
class SavingFile(SavingData):
    
    def get_full_name(self) -> str:
        return f"{self.name}{self.get_extension()}"

    def get_extension(self) -> str:
        return ".txt"


@dataclass
class Project(SavingData):
    project_path: str
    project_id: str

    def get_backup_name(self):
        return f"{self.name.lower()}_backup"

@dataclass
class Command(SavingFile):
    alias: str

    def get_extension(self) -> str:
        return ".ps1"

@dataclass
class Launcher(SavingFile):
    def get_extension(self) -> str:
        return ".cmd"