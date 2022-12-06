import time
import requests
import re
import datetime
from bs4 import BeautifulSoup
from json import JSONDecodeError
import json
from contextlib import suppress
from datetime import date


class scrap_details:

    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15'
            '(KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101'
            'Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36'
            '(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101'
            'Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            '(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

    all_lables_dict =  {'ad_id': '',
                        'ad_title': '',
                        'category': '',
                        'region': '',
                        'subregion': '',
                        'city': '',
                        'ad_price': '',
                        'private_business': '',
                        'user_id': '',
                        'make': '',
                        'model': '',
                        'generation': '',
                        'version': '',
                        'vin': '',
                        'registration': '',
                        'year': '',
                        'mileage': '',
                        'fuel_type': '',
                        'engine_capacity': '',
                        'battery_capacity': '',
                        'engine_power': '',
                        'gearbox': '',
                        'transmission': '',
                        'accident_free': '',
                        'damaged': '',
                        'condition': '',
                        'body_type': '',
                        'door_count': '',
                        'nr_seats': '',
                        'color': '',
                        'colour_type': '',
                        'alloy_wheels_type': '',
                        'headlight_lamp_type': '',
                        'country_origin': '',
                        'air_conditioning_type': '',
                        'cruisecontrol_type': '',
                        'sunblind_type': '',
                        'tyre_type': '',
                        'sunroof': '',
                        'convertible_top_type': '',
                        'upholstery_type': '',
                        'urban_consumption': '',
                        'user_status': '',
                        'vendorswarranty_date': '',
                        'price': '',
                        'sponsor_financing': '',
                        'action_name': '',
                        'env': '',
                        'monthly_payment': '',
                        'platform': '',
                        'consumption': '',
                        'co2_emissions': '',
                        'maker_warranty_km': '',
                        'down_payment': '',
                        'remaining_payments': '',
                        'residual_value': '',
                        'video': '',
                        'autonomy': '',
                        'avg_consumption': '',
                        'offer_seek': '',
                        'price_raw': '',
                        'title': ''}

    def __init__(self) -> None:
        self.session = requests.Session()
        self.today = str(date.today())
        pass

    def get_source_code(self, url):
        source_code = requests.get(url).text
        return source_code

    def get_ads_prices(self, url):
        source = self.get_source_code(url)
        soup = BeautifulSoup(source, "html.parser")
        prices_raw = soup.find_all('span', class_ = "ooa-1bmnxg7 e1b25f6f11")
        prices_clean = [price_raw.get_text()[:-4].replace(' ', '')
                        for price_raw in prices_raw]
        currencies = [price_raw.get_text()[-3:]
                      for price_raw in prices_raw]
        urls = self.get_urls(url)
        urlids = [self.get_urlid(url) for url in urls]
        update_ids = [urlid + self.today for urlid in urlids]
        return list(zip(urlids, prices_clean, currencies, update_ids))

    def get_urls(self, url):
        source_code = self.get_source_code(url)
        pattern = r'https://www.otomoto.pl/oferta/(.*?).html'
        partial_urls = set(re.findall(pattern, source_code))
        urls = [f'https://www.otomoto.pl/oferta/{partial_url}.html'
                for partial_url in partial_urls]
        return urls

    def get_dam_con_acc_urlid(self, soup_obj):
        dam_con_acc = ['', '', '']
        kwargs = [['Uszkodzony', ('Tak', 'yes'), ('Nie', 'no')],
                  ['Stan', ('Nowe','new'), ('Używane','used')],
                  ['Bezwypadkowy', ('Tak', 'yes'), ('Nie', 'no')]]
        source_params = self.get_source_params(soup_obj)
        for i in range(len(dam_con_acc)):
            with suppress(KeyError):
                dam_con_acc[i] = source_params[kwargs[i][0]]
            dam_con_acc[i] = dam_con_acc[i].replace(kwargs[i][1][0],
                                                    kwargs[i][1][1])\
                                           .replace(kwargs[i][2][0],
                                                    kwargs[i][1][1])\
                                           .replace('\n', '')\
                                           .replace(' ', '')
        parameters_dict = {'damaged': dam_con_acc[0],
                           'condition': dam_con_acc[1],
                           'accident_free': dam_con_acc[2]}
        return parameters_dict

    def get_urlid(self, url):
        id = url.rsplit('-',1)[1].rsplit('.html')[0]
        return id

    def get_currency(self, soup_obj):
        currency_raw = soup_obj.find("span", class_= "offer-price__currency")
        currency = currency_raw.get_text()
        return currency

    def get_source_params(self, soup_obj):
        labels_raw = soup_obj.find_all("span", class_ = "offer-params__label")
        values_raw = soup_obj.find_all("div", class_ = "offer-params__value")
        labels_clean = [raw_label.get_text() for raw_label in labels_raw]
        values_clean = [raw_value.get_text() for raw_value in values_raw]
        source_params_dict = dict(zip(labels_clean, values_clean))
        return source_params_dict

    def get_script_params(self, soup_obj):
        scripts = soup_obj.find_all("script", type="text/javascript")
        for script in scripts:
            if "GPT.targeting =" in script.get_text():
                json_from_script = script.get_text().split('GPT.targeting = ')
                json_from_script = json_from_script[-1].rsplit(';\n')[0]
        try:
            script_params_dict = json.loads(json_from_script)
        except json.decoder.JSONDecodeError:
            print(json_from_script)
            return
        return script_params_dict

    def get_all_params(self, soup_obj):
        con_dam_acc_params = self.get_dam_con_acc_urlid(soup_obj)
        other_params = self.get_script_params(soup_obj)
        all_params_merged = {**other_params, **con_dam_acc_params}
        params_standardized = {**self.all_lables_dict, **all_params_merged}
        params_list = list(params_standardized.values())
        params_list_flat = [params_list[i][0]
                            if type(params_list[i]) is list
                            else params_list[i]
                            for i in range(len(params_list))]
        return params_list_flat

    def change_datatypes(self, params_list):
        index_to_int = [1, 9, 16, 17, 28, 29]
        index_to_float = [7, 19, 20, 21]
        params_list = [int(params_list[i])
                            if i in index_to_int and params_list[i] != ''
                            else params_list[i]
                            for i in range(len(params_list))]
        params_list = [float(params_list[i])
                       if i in index_to_float and params_list[i] != ''
                       else params_list[i]
                       for i in range(len(params_list))]
        params_list[15] = params_list[15].upper()
        return params_list

    def get_ad_parameters(self, url):
        source_code = self.get_source_code(url)
        soup = BeautifulSoup(source_code, "html.parser")
        urlid = [self.get_urlid(url)]
        list_of_parameters = urlid + self.get_all_params(soup)
        list_of_parameters = self.change_datatypes(list_of_parameters[:42])
        list_of_parameters = [self.today] + list_of_parameters
        return list_of_parameters