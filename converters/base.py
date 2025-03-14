from abc import ABC, abstractmethod
import csv
from sqlite3 import Connection 
class DataConverter(ABC):
    data_path = ""
    data = None

    def __init__(self, data_path):
        self.data_path = data_path

    """Loads CSV file stored at data_path into variable. Data is extracted using to_tuple() method"""
    def load_data(self):
        with open(self.data_path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            self.data = list(map(lambda x: self.to_tuple(x), reader))

    """Return an insert query. Use placeholders to denote variables. This is used in conjuction with to_tuple() method"""
    @abstractmethod
    def get_query(self):
        raise NotImplementedError

    """Convert CSV data row to tuple. Tuple MUST correspond to placeholders for insert statement (denoted with ?)"""
    @abstractmethod
    def to_tuple(self, row):
        pass
    
    """Insert loaded data into the database"""
    def to_database(self, conn: Connection):
        cursor = conn.cursor()
        if self.data == None or len(self.data) == 0:
            raise Exception("Empty data")
        print(self.get_query(), self.data)
        cursor.executemany(self.get_query(), self.data)
        conn.commit()
        cursor.close()