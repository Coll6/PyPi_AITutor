import os
import sys

# Add the parent directory of main_prg to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from database.db_manager import DataManager
from utils.sensors.dht11_interface import DHTSensor

#Some way to register sensors

def print_menu():
	print("\nAvailable commands:")
	print("1, add_source - Add new measurement source.")
	print("2, test - Make and record test measurement.")
	print("3. exit - Exit the program")

def rec_meas(sensor, database):
	print('recording measurement')
	success, temp, humid, err = sensor.read_sensor_data()
	if success:
		current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		name_src = "DHT11-1"
		source_id = 1
		database.insert_data(current_time, temp, humid, name_src, source_id)
	else:
		print(f'Error: {err}')
def add_source(database):
	print('Name of source- Cannot be empty.')
	name = input('enter name:')
	if name == '':
		print('Name cannot be blank')
		return
	desc = input('Give source a description')
	type = input('What is sensor type')
	database.add_source(name, desc, type)

def main():
	sensor = DHTSensor(17)
	dbmanager = DataManager('database/tempdata.db')
	menu_active = True

	while menu_active:
		print_menu()
		command = input("\nEnter command: ").strip().lower()
		if command == "add_source":
			add_source(dbmanager)
			#database.insert_sdata()
		elif command == "test":
			rec_meas(sensor, dbmanager)
		elif command == "exit":
			#dbmanager.close()
			menu_active = False
		else:
			print(f'{command}')
if __name__== "__main__":
	main()
