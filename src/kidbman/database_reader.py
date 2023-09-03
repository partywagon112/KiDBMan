import pyodbc 
import pandas

class LibaryDatabase():
    def __init__(self, connection_string, type: str=None, dsn: str=None, username: str = None, password: str = None, timeout_seconds: int = None, *args, **kwargs):
        self.type = type
        self.dsn = dsn
        self.username = username
        self.password = password
        self.timeout_seconds = timeout_seconds
        self.connection_string = connection_string

    def __new_cursor(self) -> pyodbc.Cursor:
        connection = pyodbc.connect(self.connection_string)
        return connection.cursor()
    
    def get_table_names(self):
        cursor = self.__new_cursor()
        return [row.table_name for row in cursor.tables(tableType='TABLE')]
    
    def get_table_fields(self, table_name):
        cursor = self.__new_cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return [column[0] for column in cursor.description]

    @classmethod
    def from_source(cls, source: dict):
        return cls(**source)