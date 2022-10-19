import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent(use_cache_server=False)
headers = {'accept': '*/*', 'user-agent': ua.firefox}

result_data = []
list_url = []

url = 'https://oriencoop.cl/sucursales.htm'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

data = soup.find_all('ul', class_='sub-menu')

for i in data:
    current_url = i.find('a').get('href')
    list_url.append(current_url)


for url in list_url:

    response = requests.get(f'https://oriencoop.cl{url}', headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find('div', class_='s-dato')
    ans = data.find_all('p')

    address = ''
    latlon = []
    phones = []
    working_hours = []
    name = 'Oriencoop'

    for i in range(len(ans)):
        if i == 0:
            address = ans[i].find('span').text
        if i == 1:
            numbers = ans[i].find_all('span')
            for number in numbers:
                phones.append(number.text)
        if i == 3:
            hours = ans[i].find_all('span')
            for hour in hours:
                working_hours.append(hour.text)

    map = soup.find('div', class_='s-mapa').find('iframe').get('src')
    latlon.append(float(map.partition('2d')[2].partition('!')[0]))
    latlon.append(float(map.partition('3d')[2].partition('!')[0]))

    result_data.append(dict(
        address=address,
        latlon=latlon,
        phones=phones,
        working_hours=working_hours,
        name=name
    ))

result_data = json.dumps(result_data)
print(result_data)
