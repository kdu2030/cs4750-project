import mysql.connector
from mysql.connector import MySQLConnection
from typing import Union, List, Dict

class HooEatsDatabase:

    def __init__(self, secure:bool = False):
        HOST = "35.188.232.76"
        DATABASE = "hooeatsdb"
        USERNAME = "webappuser"
        PASSWORD = "GCFSpring2023"
        
        self.db = mysql.connector.connect(host=HOST, database=DATABASE, username=USERNAME, password=PASSWORD, autocommit=True)
        if self.db.is_connected() and secure == False:
            self.cursor = self.db.cursor(buffered=True, dictionary=True)
        elif self.db.is_connected:
            self.cursor = self.db.cursor(dictionary=True, prepared=True)
    
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
    
    def execute_secure(self, expect_results:bool, formatted_query: str, *args: List):
        self.cursor.execute(formatted_query, tuple(args))

        if not expect_results:
            return None
        return self.cursor.fetchall()

        
    
    def close(self):
        self.cursor.close()
        self.db.close()


def main():
    test_dict = {"column1": 2, "column2": "Test"}
    print(HooEatsDatabase.insert_dict("test", test_dict))
    #database.execute_sql_file("db_setup.sql", expect_results=False)
    #database.close()
    

if __name__ == "__main__":
    main()