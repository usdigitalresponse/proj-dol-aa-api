from database.db_connection import DatabaseConnection
import sys

if __name__ == "__main__":
    # Clear and remake real and/or test databases.
    if len(sys.argv) < 2:
        print("Must pass in flag for test or prod.")
    elif sys.argv[1] == "test":
        db_connection = DatabaseConnection(is_test=True)
        db_connection.reset_table()
        db_connection.close()
    elif sys.argv[1] == "prod":
        db_connection = DatabaseConnection(is_test=False)
        db_connection.reset_table()
        db_connection.close()
    else:
        print("Must pass either test or prod as flag.")
