import requests
from bs4 import BeautifulSoup

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}

url = f'https://www.dotabuff.com/heroes/meta'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'sortable no-arrows r-tab-enabled'})

l = []

for i, row in enumerate(table.find_all('tr')[3:]):
    cells = row.find('td')
    l.append(cells.get('data-value'))
print(l)


