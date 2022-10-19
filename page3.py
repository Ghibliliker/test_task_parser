import requests
from geopy import DataBC
import json


cookies = {
    'BITRIX_SM_GUEST_ID': '12159928',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1666216740%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '_ym_uid': '166616979699069138',
    '_ym_d': '1666169796',
    'BX_USER_ID': 'fec7d40e2b033199aecf89fae8fd4d15',
    '_ga': 'GA1.2.1119053725.1666169797',
    '_gid': 'GA1.2.1384138129.1666169797',
    '_ym_isad': '1',
    'PHPSESSID': 'bff82b7673515584dac9e6296df4cb96',
    '_ym_visorc': 'w',
    'BITRIX_SM_LAST_VISIT': '19.10.2022+12%3A48%3A45',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://naturasiberica.ru',
    'Referer': 'https://naturasiberica.ru/our-shops/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'type': 'all',
}

response = requests.post(
    'https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php',
    cookies=cookies,
    headers=headers,
    data=data
)

shops = response.json()['original']

result_data = []

for shop in shops:

    phones = []
    working_hours = []

    phones.append(shop['phone'])
    working_hours.append(shop['schedule'])
    address = shop['city'] + ', ' + shop['address']
    location = DataBC().geocode(address)
    latlon = [location.latitude, location.longitude]

    result_data.append(dict(
        address=address,
        latlon=latlon,
        phones=phones,
        working_hours=working_hours,
        name='Natura Siberica'
    ))
    break

result_data = json.dumps(result_data)
print(result_data)
