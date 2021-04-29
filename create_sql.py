import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

def main():

    try:
        """  
        clears the sql tables
        """
        cursor.execute("""DROP TABLE account""")
    except:
        pass
    try:
        """
        creates the sql tables with their variables
        """
        cursor.execute(""" CREATE TABLE IF NOT EXISTS  account (accountNum integer, name TEXT, pinCode TEXT,
        money integer);""")
        print("account was created")
    except:
        print("account error")
if __name__ == '__main__':
    main()
