import sqlite3
import sqlite3 as s
from pprint import pprint
from software_shop_webapp import get_current_directory


def q(cursor: sqlite3.Cursor, 
      sequel_query: str, 
      insert_values: list = None, 
      safe: bool = True, 
      print_query: bool = False) -> bool:
    """short name for SQLite3 Q-uery, the first letter, yes. Does whatever Cursor.execute() does."""
    
    if print_query:
        print(sequel_query)
    
    if safe:
        if insert_values:
            try: cursor.execute(sequel_query, insert_values)
            except: 
                print("oopsie")
                return False
            return True
        try: cursor.execute(sequel_query)
        except: return False
        return True
    if insert_values:
        cursor.execute(sequel_query, insert_values)
        return True
    cursor.execute(sequel_query)
    return True


def main() -> None:
    directory = get_current_directory()
    connection = sqlite3.connect(f'{directory}database.db')
    cur = connection.cursor()


if __name__ == "__main__":
    main()
