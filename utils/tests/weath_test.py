import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.scrape.WeathScrape import wscrape

def main():
	web = wscrape("https://weather.com/weather/today/l/40a7bf49609ca5b320e07f039c6f1bdfeadd23823655fbe416e75fd0aa25e83e")
	
	print(f'{web.scrape_data()}')

if __name__== "__main__":
	main()
