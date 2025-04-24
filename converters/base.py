import csv
from abc import ABC, abstractmethod
from typing import List, Generic

from sqlalchemy.orm import Session
from typing_extensions import TypeVar

Model = TypeVar("Model")


class DataConverter(ABC, Generic[Model]):
    data_path = ""
    data: List[Model] = []

    def __init__(self, data_path):
        self.data_path = data_path

    """Loads CSV file stored at data_path into variable. Data is extracted using to_tuple() method"""

    def load_data(self):
        with open(self.data_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            self.data = list(map(lambda x: self.to_model(x), reader))

    """Convert CSV data row to tuple. Tuple MUST correspond to placeholders for insert statement (denoted with ?)"""

    @abstractmethod
    def to_model(self, row) -> Model:
        pass

    """Insert loaded data into the database"""

    def to_database(self, session: Session):
        if len(self.data) == 0:
            raise Exception("Empty data")
        session.add_all(self.data)
        session.commit()
