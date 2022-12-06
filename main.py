from scrap_details import scrap_details
from db_connect import DbConnect
import time
import requests
import re

# regions = ['dolnoslaskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie',
#            'lodzkie', 'malopolskie', 'mazowieckie', 'opolskie', 'podkarpackie',
#            'podlaskie', 'pomorskie', 'slaskie', 'swietokrzyskie',
#            'warminsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie']

if __name__ == '__main__':

	scrap = scrap_details()
	db_con = DbConnect("oto.db")
	start = time.time()
	urls_done = []
	while True:
		urls_list = scrap.get_urls(f"https://www.otomoto.pl/osobowe?\
			search%5Border%5D=created_at_first%3Adesc&page=0\
			&search%5Badvanced_search_expanded%5D=true")
		urls_notdone = [x for x in urls_list if x not in urls_done]
		for url in urls_notdone:
			parameters = scrap.get_ad_parameters(url)
			print(parameters)
			db_con.insert_data(parameters)
			urls_done = urls_list
		time.sleep(20)


	stop = time.time()
	print(f'executed in {stop-start}')



# 	prices = scrap.get_ads_prices(f"https://www.otomoto.pl/osobowe?\
# 	search%5Border%5D=created_at_first%3Adesc&page={i}\
# 	&search%5Badvanced_search_expanded%5D=true")