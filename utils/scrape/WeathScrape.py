#https://weather.com/weather/today/l/40a7bf49609ca5b320e07f039c6f1bdfeadd23823655fbe416e75fd0aa25e83e
import requests
from bs4 import BeautifulSoup


class wscrape:
	def __init__(self, wcurl):
		self.wcurl = wcurl
	def scrape_data(self):
		response = requests.get(self.wcurl)

		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			temp = soup.find('span', class_='TodayDetailsCard--feelsLikeTempValue--2icPt').text[:-1]
			humid = soup.find('span', {'data-testid': 'PercentageValue'}).text[:-1]
			return temp, humid
		else:
			return False, False
