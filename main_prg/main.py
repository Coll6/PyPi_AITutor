import os
import sys

# Add the parent directory of main_prg to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_manager import DataManager

def main():
	dbmanager = DataManager('database/blank_database.db')
	dbmanager.insert_data("2024-09-13 10:00:00", 22.5)

if __name__== "__main__":
	main()
