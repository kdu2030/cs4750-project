import mysql.connector
from mysql.connector import MySQLConnection
from typing import Union, List, Tuple

class HooEatsDatabase:

    def __init__(self):
        HOST = "35.188.232.76"
        DATABASE = "hooeatsdb"
        USERNAME = "root"
        PASSWORD = "GCFSpring2023"
        self.db = mysql.connector.connect(host=HOST, database=DATABASE, username=USERNAME, password=PASSWORD)
        if self.db.is_connected():
            self.cursor = self.db.cursor(buffered=True)
    
    def execute_sql_file(self, file_path: str, expect_results:bool = True) -> Union[None, List[Tuple]]:
        with open(file_path, "r") as sql_file:
            self.cursor.execute(sql_file.read(), multi=True)
            self.db.commit()
        if not expect_results:
            return None
        return self.cursor.fetchall()
    
    def execute(self, query: str, expect_results:bool = True) -> Union[None, List[Tuple]]:
        self.cursor.execute(query)
        self.db.commit()
        if not expect_results:
            return None
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.db.close()


def main():
    database = HooEatsDatabase()
    database.execute_sql_file("db_setup.sql")
    database.close()
    

if __name__ == "__main__":
    main()