import mysql.connector
from mysql.connector import MySQLConnection
from typing import Union, List, Dict

class HooEatsDatabase:

    def __init__(self):
        HOST = "35.188.232.76"
        DATABASE = "hooeatsdb"
        USERNAME = "root"
        PASSWORD = "GCFSpring2023"
        # HOST  = "mysql01.cs.virginia.edu"
        # DATABASE = "kd5eyn_c"
        # USERNAME = "kd5eyn"
        # PASSWORD = "GCFSpring2023"

        self.db = mysql.connector.connect(host=HOST, database=DATABASE, username=USERNAME, password=PASSWORD, autocommit=True)
        if self.db.is_connected():
            self.cursor = self.db.cursor(buffered=True, dictionary=True)
    
    def execute_sql_file(self, file_path: str, expect_results:bool = True) -> Union[None, List[Dict]]:
        with open(file_path, "r") as sql_file:
            self.cursor.execute(sql_file.read(), multi=True)
        if not expect_results:
            return None
        return self.cursor.fetchall()
    
    def execute(self, query: str, expect_results:bool = True) -> Union[None, List[Dict]]:
        self.cursor.execute(query)
        if not expect_results:
            return None
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.db.close()


def main():
    database = HooEatsDatabase()
    database.execute_sql_file("db_setup.sql", expect_results=False)
    database.close()
    

if __name__ == "__main__":
    main()