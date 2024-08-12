import json
from abc import ABC, abstractmethod
from typing import List
from bench.data.models import DataItem


class BaseData(ABC):
    def __init__(self):
        self.data_items: List[DataItem] = []

    def add_data_items(self, items: List[DataItem]):
        self.data_items.extend(items)

    @abstractmethod
    def parse(self, url: str) -> List[DataItem]:
        pass

    def save(self, file_path=str) -> None:
        with open(file_path, "w") as json_file:
            json_data = [item.model_dump() for item in self.data_items]
            json.dump(json_data, json_file, indent=4)
