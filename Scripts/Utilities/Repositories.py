from collections.abc import Callable
from uuid import UUID
from Scripts.Utilities.SavingData import SavingData, SavingFile
from config import Config
from pathlib import Path
import subprocess

class ObjectRepository[T : SavingData]:
    def __init__(
        self,
        key: str,
        item_type: type[T]
    ):
        self.saver = None
        self.key = key
        self.item_type = item_type
        self.callbacks: dict[str, Callable[[T], None]] = {}

    def add_callback(
        self,
        func: Callable,
        callback: Callable[[T], None]
    ):
        self.callbacks[func.__name__] = callback

    def remove_callback(self, name: str):
        self.callbacks.pop(name, None)

    def check_callback(self, func: Callable, item: T):
        callback = self.callbacks.get(func.__name__)

        if callback is not None:
            callback(item)

    def has_item(self, id: UUID) -> bool:
        for data in self.saver.get_data().get(self.key) or []:
            if self.item_type.from_dict(data).uuid == id:
                return True
        return False

    def get_item(self, id:UUID):
        for data in self.saver.get_data().get(self.key) or []:
            it = self.item_type.from_dict(data) 
            if it.uuid == id:
                return True
        return None

    def add_item(self, item: T):
        if self.has_item(item.uuid):
            return

        data = self.saver.get_data()
        items = data.get(self.key) or []

        items.append(item.to_dict())
        data[self.key] = items

        self.saver.save(data)

        self.check_callback(self.add_item, item)

    def remove_item(self, id: UUID):
        data = self.saver.get_data()
        items = data.get(self.key) or []

        item = self.get_item(id)
        if not item == None:
            items.remove(item)

        data[self.key] = items
        self.saver.save(data)

    def get_items(self) -> list[T]:
        items = self.saver.get_data().get(self.key) or []

        return [
            self.item_type.from_dict(item)
            for item in items
        ]

class FileRepository[T : SavingFile](ObjectRepository[T]):
    def __init__(self, dir: str, key:str, item_type:type[T]):
        super().__init__(key, item_type)
        self.directory = dir
        path = Path(Config.get_property("storage_dir_path")) / dir
        path.mkdir(exist_ok=True)
        
    def get_path(self, item:T) -> Path:
        return Path(Config.get_property("storage_dir_path")) / self.directory / item.get_full_name()

    def open_file(self, item:T):
        file_path = self.get_path(item)
        if not file_path.exists():
            file_path.touch()
        subprocess.Popen([Config.get_property("vs_code_path"), str(file_path)])

    def get_file_text(self, item:T):
        with open(self.get_path(item), "r") as f:
            full_text = ""
            for line in f.readlines():
                full_text += line
        return full_text


    
    def add_item(self, item: T):
        path = self.get_path(item)
        path.touch(exist_ok=True)

        super().add_item(item)

    def remove_item(self, id: UUID):
        item = self.get_item(id)
        self.get_path(item).unlink(missing_ok=True)

        super().remove_item(id)