import time
import os
import sys
import threading

# Add the parent directory of main_prg to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from database.db_manager import DataManager
from utils.sensors.dht11_interface import DHTSensor
from utils.scrape.WeathScrape import wscrape
#Some way to register sensors

#Define sensors for auto measurements
meas_list = {
	1 : { "name" : "DHT11-1", "interval" : 60, "read_function" : "dht11", "last_checked" : 0, "interface" : None},
	2 : { "name" : "WeatherChannel-https://weather.com/weather/today/l/40a7bf49609ca5b320e07f039c6f1bdfeadd23823655fbe416e75fd0aa25e83e", "interval" : 300, "read_function" : "WeathScrape", "last_checked" : 0, "interface" : None}
}

def print_menu():
	print("\nAvailable commands:")
	print("1, add_source - Add new measurement source.")
	print("2, test - Make and record test measurement.")
	print("3, auto - Start auto measurements.")
	print("4, stop - Stop auto measurements.")
	print("5. exit - Exit the program")

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
def rec_api(database, scrape, id):
	temp, humid, suc = scrape.scrape_data()
	if temp is not None:
		current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		name_src = "WeatherChannel"
		source_id = 2
		tempc = round((int(temp) - 32)*(5/9), 1)
		database.insert_data(current_time, tempc,int(humid), name_src, source_id)
def proc_auto(dic_list, event, dbmanager):
	while True:
		for interface_id, interface  in dic_list.items():
			temp = None
			humid = None
			cur_time = datetime.now()
			if interface["last_checked"] == 0:
				interface["last_checked"] = datetime.now() - timedelta(seconds = interface["interval"])
			if (datetime.now() - interface["last_checked"]) >= timedelta(seconds = interface["interval"]):
				read_with = interface["read_function"]
				if read_with == "dht11":
					suc, temp, humid, err = interface["interface"].read_sensor_data()
					if suc:
						#tempc = round((int(temp) - 32)*(5/9), 1)
						dbmanager.insert_data(cur_time.strftime('%Y-%m-%d %H:%M:%S'), temp, int(humid), interface["name"], interface_id)
						interface["last_checked"] = cur_time
					else: print(f'{interface["name"]} interface has failed. Will attempt again.')
				elif read_with == "WeathScrape":
					temp, humid, suc = interface["interface"].scrape_data()
					if suc:
						tempc = round((int(temp) - 32)*(5/9), 1)
						dbmanager.insert_data(cur_time.strftime('%Y-%m-%d %H:%M:%S'), tempc, int(humid), interface["name"].split('-')[0], interface_id)
						interface["last_checked"] = cur_time
					else: print(f'{interface["name"]} interface has failed. Will attempt again.')
				else:
					print("Unknown read interface.")
		if event.is_set():
			event.clear() #Allow the auto list to be allowed to start again.
			break
		time.sleep(1)
def main():
	#Setup sensors and DB
	sensor = DHTSensor(17)
	scrape = wscrape("https://weather.com/weather/today/l/40a7bf49609ca5b320e07f039c6f1bdfeadd23823655fbe416e75fd0aa25e83e")
	dbmanager = DataManager('database/tempdata.db')

	#attach interface with sensor if required
	meas_list[1]["interface"] = sensor 
	meas_list[2]["interface"] = scrape

	event = threading.Event()
	list_thread = threading.Thread(target=proc_auto, args=(meas_list,event,dbmanager,))

	menu_active = True

	while menu_active:
		print_menu()
		command = input("\nEnter command: ").strip().lower()
		if command == "add_source":
			add_source(dbmanager)
			#database.insert_sdata()
		elif command == "test":
			rec_meas(sensor, dbmanager)
			rec_api(dbmanager, scrape, 2)
		elif command == "exit":
			#dbmanager.close()
			event.set()
			menu_active = False
		elif command == "auto":
			list_thread.start()
		elif command == "stop":
			event.set()
		else:
			print(f'Not Valid command: {command}')
if __name__== "__main__":
	main()
