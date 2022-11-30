from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
import time


regions = ['dolnoslaskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie', 'lodzkie', 'malopolskie', 'mazowieckie', 'opolskie', 
           'podkarpackie', 'podlaskie', 'pomorskie', 'slaskie', 'swietokrzyskie', 'warminsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie']

all_params_labels = {'Oferta od': 'null', 'Kategoria': 'null', 'Marka pojazdu': 'null', 'Model pojazdu': 'null', 'Wersja': 'null', 
                     'Generacja': 'null', 'Rok produkcji': 'null', 'Przebieg': 'null', 'Pojemność skokowa': 'null', 'Rodzaj paliwa': 'null', 
                     'Moc': 'null', 'Skrzynia biegów': 'null', 'Napęd': 'null', 'Filtr cząstek stałych': 'null', 'Spalanie W Cyklu Mieszanym': 'null', 
                     'Spalanie Poza Miastem': 'null', 'Spalanie W Mieście': 'null', 'Typ nadwozia': 'null', 'Emisja CO2': 'null', 'Liczba drzwi': 'null', 
                     'Liczba miejsc': 'null', 'Kolor': 'null', 'Rodzaj koloru': 'null', 'VAT marża': 'null', 'Możliwość finansowania': 'null', 
                     'Faktura VAT': 'null', 'Leasing': 'null', 'Kraj pochodzenia': 'null', 'Pierwsza rejestracja': 'null', 'Numer rejestracyjny pojazdu': 'null', 
                     'Zarejestrowany w Polsce': 'null', ' Pierwszy właściciel (od nowości)': 'null', 'Bezwypadkowy': 'null', 'Serwisowany w ASO': 'null', 
                     'Stan': 'null', 'Uszkodzony': 'null', 'Okres gwarancji producenta': 'null', 'lub do (przebieg km)': 'null',  
                     'Autonomia': 'null', 'Tuning': 'null', 'Homologacja ciężarowa': 'null', 'Kierownica po prawej (Anglik)': 'null', 
                     'Pokaż oferty z numerem VIN': 'null', 'Ma numer rejestracyjny': 'null', 'VIN': 'null', 'Miesięczna rata': 'null',}

def get_params(url):
    try:
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        ad_id = soup.find_all("span", class_="offer-meta__value")[1].get_text()
        price_number = soup.find("span", class_="offer-price__number").get_text().replace('\n','')[:9].replace(' ', '')
        currency = soup.find("span", class_="offer-price__number").get_text().replace('\n','')[-3:]
        vin = soup.find_all("script", type="text/javascript")[16].get_text().split(',"vin":["')[-1].rsplit('"')[0]
        params_label_raw = soup.find_all("span", class_="offer-params__label")
        params_value_raw = soup.find_all("div", class_="offer-params__value")
        features_raw = soup.find_all("li", class_="parameter-feature-item")
        params_label_clean = [x.get_text() for x in params_label_raw]
        params_value_clean = [x.get_text().replace('\n','').replace('  ', '') for x in params_value_raw]
        features_clean = [x.get_text().replace('\n','').replace('  ', '') for x in features_raw]
        params_dict = dict(zip(params_label_clean, params_value_clean))
        params_merged = {**all_params_labels, **params_dict}
        # print(vin)
        # print(currency)
        # print(price_number)
        # print(ad_id)
        print(params_merged)
        print(len(params_merged))
        # print(features_clean)
        return len(params_merged)
    except Exception as e:
        return e

start = time.time()

for i in range(30):
    r = requests.get(f"https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page={i}&search%5Badvanced_search_expanded%5D=true")
    source = r.text
    urls = set(re.findall( r'https://www.otomoto.pl/oferta/(.*?).html', source))
    print(len(urls))
    start = time.time()
    for i in urls:
        a = get_params(f'https://www.otomoto.pl/oferta/{i}.html')
        if a > 46:
            break
    else:
        continue
    break

stop = time.time()
print(f'executed in {stop-start}')