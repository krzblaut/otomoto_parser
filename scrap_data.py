import requests
import re
from bs4 import BeautifulSoup
from json import JSONDecodeError
import json
from contextlib import suppress


class scrap_data:

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
                        'title': '',
                        'ad_title': '',
                        'private_business': '',
                        'category': '',
                        'region': '',
                        'subregion': '',
                        'ad_price': '',
                        'user_id': '',
                        'city': '',
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
                        'price_raw': '',}

    def __init__(self) -> None:
        self.session = requests.Session()
        pass

    def get_source_code(self, url):
        source_code = requests.get(url).text
        return source_code

    def get_urls(self, url):
        source_code = self.get_source_code(url)
        pattern = r'https://www.otomoto.pl/oferta/(.*?).html'
        partial_urls = set(re.findall(pattern, source_code))
        urls = [f'https://www.otomoto.pl/oferta/{partial_url}.html'
                for partial_url in partial_urls]
        return urls

    def get_con_dam_acc_params(self, soup_obj):
        acc_free = ''
        damaged = ''
        condition = ''
        labels_raw = soup_obj.find_all("span", class_ = "offer-params__label")
        values_raw = soup_obj.find_all("div", class_ = "offer-params__value")
        labels_clean = [raw_label.get_text() for raw_label in labels_raw]
        values_clean = [raw_value.get_text() for raw_value in values_raw]
        labels_values_dict = dict(zip(labels_clean, values_clean))
        with suppress(KeyError): acc_free = labels_values_dict['Bezwypadkowy']
        with suppress(KeyError): damaged = labels_values_dict['Uszkodzony']
        with suppress(KeyError): condition = labels_values_dict['Stan']
        damaged = damaged.replace('Tak', 'yes').replace('Nie', 'no')\
            .replace('\n', '').replace(' ', '')
        condition = condition.replace('Nowe','new').replace('Używane','used')\
            .replace('\n', '').replace(' ', '')
        acc_free = acc_free.replace('Tak', 'yes').replace('Nie', 'no')\
            .replace('\n', '').replace(' ', '')
        parameters_dict = {'accident_free': acc_free,
                           'damaged': damaged,
                           'condition': condition}
        return parameters_dict

    def get_other_params(self, soup_object):
        script_string = soup_object.find_all("script", type="text/javascript")
        json_from_script = script_string[16].get_text().split('GPT.targeting = ')
        json_from_script = json_from_script[-1].rsplit(';\n')[0]
        parameters_dict = json.loads(json_from_script)
        return parameters_dict

    def get_all_params(self, soup_object):
        con_dam_acc_params = self.get_con_dam_acc_params(soup_object)
        other_params = self.get_other_params(soup_object)
        all_params_merged = {**other_params, **con_dam_acc_params}
        params_standardized = {**self.all_lables_dict, **all_params_merged}
        params_list = list(params_standardized.values())
        return params_list

    def get_ad_parameters(self, url):
        source_code = self.get_source_code(url)
        soup = BeautifulSoup(source_code, "html.parser")
        list_of_parameters = self.get_all_params(soup)
        return list_of_parameters
