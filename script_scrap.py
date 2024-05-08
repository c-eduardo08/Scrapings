import requests
from bs4 import BeautifulSoup
import re
import math
import pandas as pd


url = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'

#headers = your headers
#headers=headers
site = requests.get(url)
soup = BeautifulSoup(site.content, 'html.parser')

qts_itens = soup.find('div', id='listingCount').getText().strip()

#print(qts_itens)
index = qts_itens.find(' ')
qtd = qts_itens[:index]

# print(index)
print(qtd)

ultima_pagina = math.ceil(int(qtd)/ 20)

dic_produtos = {'marca':[], 'preco':[]}

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('article', class_=re.compile('productCard'))
    
    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).getText().strip()
        # preco = produto.find('span', class_=re.compile('availablePricesCard')).find('span', class_=re.compile('priceCard')).getText().strip()
        # preco = produto.find('span', class_=re.compile('priceCard')).getText().strip()

        # add preco

        print(marca)
        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(0)

    print(url_pag)

df = pd.DataFrame(dic_produtos)
df.to_csv('preco-cadeira.csv', encoding="utf-8", sep=";")
