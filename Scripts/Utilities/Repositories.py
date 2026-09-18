from collections.abc import Callable
from uuid import UUID


class ObjectRepository[T]:
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

        for raw_item in items:
            item = self.item_type.from_dict(raw_item)

            if item.uuid == id:
                items.remove(raw_item)
                break

        data[self.key] = items
        self.saver.save(data)

    def get_items(self) -> list[T]:
        items = self.saver.get_data().get(self.key) or []

        return [
            self.item_type.from_dict(item)
            for item in items
        ]


class File[T](ObjectRepository[T]):
    def __init__(self, dir: str, key:str, item_type:type[T]):
        super().__init__(key, item_type)
        self.directory = dir


    def add_item(self, item: T):

        super().add_item(item)


