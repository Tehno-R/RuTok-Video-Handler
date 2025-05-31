import uuid
from typing import Set

import Logger

logger = Logger.generate_logger("IDController")

class IdController:
    _storage: Set[str] = set()

    def __init__(self):
        raise TypeError("Нельзя создавать экземпляры статического класса")

    @staticmethod
    def generate_unique_id() -> str:
        while True:
            new_id = str(uuid.uuid4())
            if new_id not in IdController._storage:
                IdController._storage.add(new_id)
                return new_id

    @staticmethod
    def delete_unique_id(id_to_delete: str):
        if id_to_delete not in IdController._storage:
            logger.error(f"Error deleting id '{id_to_delete}' from storage")
        else:
            IdController._storage.remove(id_to_delete)
