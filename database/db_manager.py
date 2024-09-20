#Temp data schema
#id(integer)-timestamp(datetime)-temp_c(real)-source(text)-additional_info(text)
import os
import sqlite3

class DataManager:
	def __init__(self, db_dir):
		self.database = db_dir
		self._initialize_db()
 #_signifies an internal function dont use outside class
	def _create_tables(self, conn):
		conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support
		conn.execute("""
			CREATE TABLE IF NOT EXISTS sources (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				source_name TEXT NOT NULL,
				description TEXT,
				sensor_type TEXT
			)
		""")
		conn.execute("""
			CREATE TABLE IF NOT EXISTS TempHumData (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
				temperature REAL,
				humidity REAL,
				source TEXT,
				source_id INTEGER,
				FOREIGN KEY (source_id) REFERENCES sources(id)
			)
		 """)
	def _is_valid_file(self, file_path):
		with open(file_path, 'rb') as file: #Opens
			header = file.read(16)
			print(f'{header}')
			return header == b'SQLite format 3\x00'
	def _create_database(self, file):
		with sqlite3.connect(file) as conn:
			self._create_tables(conn)
	def _initialize_db(self):
		if not os.path.exists(self.database) or not self._is_valid_file(self.database):
			print(f'{self.database} does not exist. Creating database')
			self._create_database(self.database)
		else:
			print(f'{self.database} exists using file.')
	def insert_data(self, timestamp, temp, humid, name_src, source_id):
		with sqlite3.connect(self.database) as conn:
			conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support
			cursor = conn.cursor()
			cursor.execute("""
				INSERT INTO TempHumData (timestamp, temperature, humidity, source, source_id)
				VALUES(?, ?, ?, ?, ?)
			""", (timestamp, temp, humid, name_src, source_id))
			conn.commit()
			print("Data added.")
	def add_source(self, name, descrip, type):
		with sqlite3.connect(self.database) as conn:
			cursor = conn.cursor()
			cursor.execute("""
				INSERT INTO sources (source_name, description, sensor_type)
				VALUES (?, ?, ?)
				""", (name, descrip, type))
			conn.commit()

