from scrap_data import scrap_data
import time
import requests
import re

# regions = ['dolnoslaskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie',
#            'lodzkie', 'malopolskie', 'mazowieckie', 'opolskie', 'podkarpackie',
#            'podlaskie', 'pomorskie', 'slaskie', 'swietokrzyskie',
#            'warminsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie']

# all_lables_dict =  {'ad_id': '',
# 					'title': '',
# 					'ad_title': '',
# 					'offer_seek': '',
# 					'private_business': '',
# 					'category': '',
# 					'region': '',
# 					'subregion': '',
# 					'ad_price': '',
# 					'user_id': '',
# 					'city': '',
# 					'make': '',
# 					'model': '',
# 					'generation': '',
# 					'version': '',
# 					'vin': '',
# 					'registration': '',
# 					'year': '',
# 					'mileage': '',
# 					'fuel_type': '',
# 					'engine_capacity': '',
# 					'battery_capacity': '',
# 					'engine_power': '',
# 					'gearbox': '',
# 					'transmission': '',
# 					'accident_free': '',
# 					'damaged': '',
# 					'condition': '',
# 					'body_type': '',
# 					'door_count': '',
# 					'nr_seats': '',
# 					'color': '',
# 					'colour_type': '',
# 					'price_raw': '',
# 					'alloy_wheels_type': '',
# 					'headlight_lamp_type': '',
# 					'country_origin': '',
# 					'air_conditioning_type': '',
# 					'cruisecontrol_type': '',
# 					'sunblind_type': '',
# 					'tyre_type': '',
# 					'sunroof': '',
# 					'convertible_top_type': '',
# 					'upholstery_type': '',
# 					'urban_consumption': '',
# 					'user_status': '',
# 					'vendorswarranty_date': '',
# 					'price': '',
# 					'sponsor_financing': '',
# 					'action_name': '',
# 					'env': '',
# 					'monthly_payment': '',
# 					'platform': '',
# 					'consumption': '',
# 					'co2_emissions': '',
# 					'maker_warranty_km': '',
# 					'down_payment': '',
# 					'remaining_payments': '',
# 					'residual_value': '',
# 					'video': '',
# 					'autonomy': '',
#      				'avg_consumption': ''}


# source_code = requests.get(url).text
# soup = BeautifulSoup(source_code, "html.parser")


# def get_condition_damaged_accident(soup_obj):
#     acc_free = ''
#     damaged = ''
#     condition = ''
#     labels_raw = soup_obj.find_all("span", class_ = "offer-params__label")
#     values_raw = soup_obj.find_all("div", class_ = "offer-params__value")
#     labels_clean = [raw_label.get_text() for raw_label in labels_raw]
#     values_clean = [raw_value.get_text() for raw_value in values_raw]
#     labels_values_dict = dict(zip(labels_clean, values_clean))
#     with suppress(KeyError): acc_free = labels_values_dict['Bezwypadkowy']
#     with suppress(KeyError): damaged = labels_values_dict['Uszkodzony']
#     with suppress(KeyError): condition = labels_values_dict['Stan']
#     damaged = damaged.replace('Tak', 'yes').replace('Nie', 'no')\
#         .replace('\n', '').replace(' ', '')
#     condition = condition.replace('Nowe', 'new').replace('Używane', 'used')\
#         .replace('\n', '').replace(' ', '')
#     acc_free = acc_free.replace('Tak', 'yes').replace('Nie', 'no')\
#         .replace('\n', '').replace(' ', '')
#     params = {'accident_free': acc_free,
#               'damaged': damaged,
#               'condition': condition}
#     return params

# def get_standardized_params_dict(soup_object):
# 	script_string = soup_object.find_all("script", type="text/javascript")
# 	json_from_script = script_string[16].get_text().split('GPT.targeting = ')
# 	json_from_script = json_from_script[-1].rsplit(';\n')[0]
# 	parameters_dict = json.loads(json_from_script)
# 	additional_params_dict = get_condition_damaged_accident(soup_object)
# 	parameters_added_dict =	{**parameters_dict, **additional_params_dict}
# 	params_standardized = {**all_lables_dict, **parameters_added_dict}
# 	return params_standardized

# url1 = "https://www.otomoto.pl/oferta/skoda-kodiaq-salon-polska\
#     -bezwypadkowy-webasto-ID6F8sBZ.html"

# i=2
# url2 = "https://www.otomoto.pl/osobowe?\
#         search%5Border%5D=created_at_first%3Adesc&page=2\
#         &search%5Badvanced_search_expanded%5D=true"

# def get_source_code(url):
# 	source_code = requests.get(url).text
# 	return source_code

# def get_urls(url):
#         source_code = get_source_code(url)
#         partial_urls = set(re.findall( r'https://www.otomoto.pl/oferta/(.*?).html', source_code))
#         urls = [f'https://www.otomoto.pl/oferta/{partial_url}.html' for partial_url in partial_urls]
#         return print(urls)

scrap = scrap_data()

# print(scrap.get_urls(url2))

start = time.time()
for i in range(1):
    urls_list = scrap.get_urls(f"https://www.otomoto.pl/osobowe?\
        search%5Border%5D=created_at_first%3Adesc&page={i}\
        &search%5Badvanced_search_expanded%5D=true")
    for url in urls_list:
        print(url)
        parameters = scrap.get_ad_parameters(url)

stop = time.time()
print(f'executed in {stop-start}')



#     partial_urls = set(re.findall( r'https://www.otomoto.pl/oferta/(.*?).html',
#                                   source_code))
#     for partial_url in partial_urls:
#         full_url = f'https://www.otomoto.pl/oferta/{partial_url}.html'
#         source_code = requests.get(full_url).text
#         soup = BeautifulSoup(source_code, "html.parser")
#         params_list = get_standardized_params_dict(soup)
#         print(params_list)
#         print(len(params_list))
#         if len(params_list) > 62:
#             break
#     else:
#         continue
#     break

# stop = time.time()
# print(f'executed in {stop-start}')





# all_params_labels = {'Oferta od': '',
#                      'Kategoria': '',
#                      'Marka pojazdu': '',
#                      'Model pojazdu': '',
#                      'Wersja': '',
#                      'Generacja': '',
#                      'Rok produkcji': '',
#                      'Przebieg': '',
#                      'Pojemność skokowa': '',
#                      'Rodzaj paliwa': '',
#                      'Moc': '',
#                      'Skrzynia biegów': '',
#                      'Napęd': '',
#                      'Filtr cząstek stałych': '',
#                      'Spalanie W Cyklu Mieszanym': '',
#                      'Spalanie Poza Miastem': '',
#                      'Spalanie W Mieście': '',
#                      'Typ nadwozia': '',
#                      'Emisja CO2': '',
#                      'Liczba drzwi': '',
#                      'Liczba miejsc': '',
#                      'Kolor': '',
#                      'Rodzaj koloru': '',
#                      'VAT marża': '',
#                      'Możliwość finansowania': '',
#                      'Faktura VAT': '',
#                      'Leasing': '',
#                      'Kraj pochodzenia': '',
#                      'Pierwsza rejestracja': '',
#                      'Numer rejestracyjny pojazdu': '',
#                      'Zarejestrowany w Polsce': '',
#                      ' Pierwszy właściciel (od nowości)': '',
#                      'Bezwypadkowy': '',
#                      'Serwisowany w ASO': '',
#                      'Stan': '',
#                      'Uszkodzony': '',
#                      'Okres gwarancji producenta': '',
#                      'lub do (przebieg km)': '',
#                      'Autonomia': '',
#                      'Pojemność baterii': '',
#                      'Rodzaj własności baterii': '',
#                      'Tuning': '',
#                      'Homologacja ciężarowa': '',
#                      'Kierownica po prawej (Anglik)': '',
#                      'Opłata początkowa': '',
#                      'Liczba pozostałych rat': '',
#                      'Wartość wykupu': '',
#                      'Pokaż oferty z numerem VIN': '',
#                      'Ma numer rejestracyjny': '',
#                      'VIN': '',
#                      'Miesięczna rata': '',
#                      'Gwarancja dealerska (w cenie)': ''}


# def get_params(soup_object):
# 	params_label_raw = soup_object.find_all("span", class_="offer-params__label")
# 	params_value_raw = soup_object.find_all("div", class_="offer-params__value")
# 	params_label_clean = [x.get_text() for x in params_label_raw]
# 	params_value_clean = [x.get_text().replace('\n','').replace('  ', '') for x in params_value_raw]
# 	params_label_value_dict = dict(zip(params_label_clean, params_value_clean))
# 	return

# def get_features(soup_object):
# 	features_raw = soup_object.find_all("li", class_="parameter-feature-item")
# 	features_clean_list = [x.get_text().replace('\n','').replace('  ', '') for x in features_raw]
# 	return features_clean_list

# def get_params(soup_object):
# 	params_label_raw = soup_object.find_all("span", class_="offer-params__label")
# 	params_value_raw = soup_object.find_all("div", class_="offer-params__value")
# 	params_label_clean = [x.get_text() for x in params_label_raw]
# 	params_value_clean = [x.get_text().replace('\n','').replace('  ', '') for x in params_value_raw]
# 	params_label_value_dict = dict(zip(params_label_clean, params_value_clean))
# 	params_merged = {**all_params_labels, **params_label_value_dict}
# 	params_values_list = list(params_merged.values())
# 	print(params_merged)
# 	return params_merged

# def clean_params(list_of_params):
# 	list_of_params[6] = int(list_of_params[6])
# 	list_of_params[7] = int(list_of_params[7].replace(' km', '').replace(' ', ''))
# 	list_of_params[8] = int(list_of_params[8].replace(' cm3', '').replace(' ', ''))
# 	list_of_params[10] = int(list_of_params[10].replace(' KM', '').replace(' ', ''))
# 	list_of_params[16] = float(list_of_params[16].replace(' l/100km', '').replace(',', '.'))
# 	return list_of_params

# def get_info(soup_object):
#     ad_id = soup_object.find_all("span", class_="offer-meta__value")
#     ad_id = ad_id[1].get_text()
#     price_number = soup_object.find("span", class_="offer-price__number")
#     price_number = price_number.get_text().replace('\n','')[:9].replace(' ', '')
#     currency = soup_object.find("span", class_="offer-price__number").get_text().replace('\n','')[-3:]
#     vin = soup_object.find_all("script", type="text/javascript")[16].get_text().split(',"vin":["')[-1].rsplit('"')[0]
#     return [ad_id, price_number, currency, vin]