import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent(use_cache_server=False)
headers = {'accept': '*/*', 'user-agent': ua.firefox}


result_data = []
list_id = []
list_url = []

url = 'https://som1.ru/shops/'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

data = soup.find_all('div', class_='col-sm-12')

for i in data:
    current_url = i.find('input').get('id')
    if current_url is not None and len(current_url) == 4:
        list_id.append(current_url)

for id in list_id:

    response = requests.get(f'https://som1.ru/shops/?CITY_ID={id}', headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find_all('div', class_='shops-col shops-button')

    for i in data:
        list_url.append(i.find('a').get('href'))


for url in list_url:

    url = f'https://som1.ru{url}'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    address = ''
    latlon = []
    phones = []
    working_hours = []

    name = soup.find('div', class_='page-body').find('h1').text

    data = soup.find('div', class_='col-md-6 col-xs-12')

    ans = data.find_all('tr')

    for i in range(len(ans)):
        if i == 0:
            address = ans[i].find_all('td')[2].text
        if i == 1:
            numbers = ans[i].find_all('td')[2].text
            numbers = numbers.split(',')
            for number in numbers:
                phones.append(number)
        if i == 2:
            hours = ans[i].find_all('td')[2].text
            hours = hours.split(',')
            for hour in hours:
                working_hours.append(hour)

    map = response.text.partition('showShopsMap([')[2].partition('}')[0].partition(':[')[2].partition('],')[0].split(',')
    latlon.append(float(map[0].strip("'")))
    latlon.append(float(map[1].strip("'")))

    result_data.append(dict(
        address=address,
        latlon=latlon,
        phones=phones,
        working_hours=working_hours,
        name=name
    ))

result_data = json.dumps(result_data)
print(result_data)
