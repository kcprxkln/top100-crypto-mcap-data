import requests 
from bs4 import BeautifulSoup
import time
import csv

def get_endpoints():
    response = requests.get('https://coinmarketcap.com/historical/')
    soup = BeautifulSoup(response.text, 'html.parser')
    endpoints = [link.get('href') for link in soup.find_all(name='a', class_='historical-link cmc-link')]
    return endpoints

def sum_snapshot_mcap(url : str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mcap_data = soup.find_all(name='td', class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap")
    mc_sum = 0 
    i = 0
    for crypto_mcap in mcap_data:
        print(crypto_mcap)
        if i == 100:
            break
        o = crypto_mcap.find('div').getText()
        o = int(o[1:-3].replace(",", ""))
        print(f'one record: {o}')
        mc_sum += o
        print(mc_sum)
        i += 1
    return mc_sum        

new_rows = []
for endpoint in get_endpoints():
    print(endpoint)
    value = sum_snapshot_mcap(f'https://coinmarketcap.com{endpoint}')
    print(value)
    day = endpoint.split("/")[2]
    new_row = [day, value]
    new_rows.append(new_row)
    print(new_rows)
    time.sleep(30)

with open('mcap_data', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in new_rows:
        writer.writerow(row)