from pathlib import Path
import json

class Config:
    config_file:str = "config.json"

    @classmethod
    def _save(cls, dataToSave):
        path = cls.get_config()
        print(path)
        with open(path, "w") as f:
            json.dump(dataToSave, f, indent=4)
    @classmethod
    def get_config(cls) -> Path:
         return Path("default_data") / cls.config_file

    @classmethod
    def _get_data(cls):
        path = cls.get_config()
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} 
    
    @classmethod
    def get_property(cls, tag:str):
        data = cls._get_data()
        return data.get(tag) or ""

    @classmethod
    def set_property(cls, tag:str, value:str):
        data = cls._get_data()
        data[tag] = value
        cls._save(data)

    @classmethod
    def initialize_storage_dir(cls, path_to_place:str):
        path = Path(path_to_place)
        path.mkdir(exist_ok=True, parents=True)
        
        cls.set_property("storage_dir_path", path_to_place)
