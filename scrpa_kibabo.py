"""
Esse programa tem a função de fazer um Web Scrapping na pagina do kibabo e retornar as informações dos produtos alimentares, ira ser feito em uma função que vai pegar os dados, e armazenar em um arquivo csv.
"""

# Vamos começando importando todos os modulos que vamos utilizar no nosso código:
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
import csv


# Vamos começar pegando os dados da pagina do kibabo
# Conectando com a pagina
url = 'https://www.kibabo.co.ao/pt/alimentar/arrozmassasfarinha/arroz-branco_850-235.html'

# buscando o headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"}

# pegando a pagina
page = requests.get(url=url,headers=headers)

# Criando um ficheiro csv
ficheiro = 'kibabo_prod_Alimentar.csv'

# pegando a pagina
soup1 = BeautifulSoup(page.content,"html.parser")

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser') #Esse é uma forma de pegar a mesma pagina, mas de uma forma mais compreensiva

# Vamos criar o cabeçalho do ficheiro csv
def head_csv():
    """Cria um Ficheiro CSV caso ele não exista, com os seguintes cabeçarios: 'Data','Nome_produto','Descrição','Tipo','Preço'

    Caso já exista, apenas rescreve o ficheiro

    """
    header = ['Data','Nome_produto','Descrição','Tipo','Preço']

    # criando um ficheiro csv
    with open(ficheiro,'w',newline='',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Vamos criar uma função CSV que vai ser responsavel por adicionar os dados recebidos em uma nova linha.

def add_csv(file:str,a:str,b:str,c:str,d:str):
    """Esta função recebe um ficheiro, que representa os dados: 'Data','Nome_produto','Descrição','Tipo','Preço'
    e adiciona os elementos a, b,c,d nele adiciona em uma nova linha esses dados"""
    data = datetime.date.today()
    l = [data,a,b,c,d]
    with open(file,'+a',newline='',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(l)


"""
Uma vez com a pagina , vamos pegar os todos os link que tem haver com os produtos alimenticios
"""

def pegar_dados():
    """Pega dados dos produtos do site do supermercado Kibabo"""
    pags = soup2.find_all('li',attrs={'class':['li-accordion', 'sel' 'initial' 'rdc-featured-li']})
    for links in pags:
        for link in links.find_all('a')[1:]:
            tipo = link.get_text().strip()
            url = link.get('href')
            page = requests.get(url=url,headers=headers)
            new_soup = BeautifulSoup(page.content,"html.parser")
            new_soup = BeautifulSoup(new_soup.prettify(), 'html.parser')
            for produto in new_soup.find_all('div',attrs={'class':'col-sm-3'}):
                marca = produto.find('p',attrs={'class':'key1-name'}).text.strip()
                descricao = produto.find('p',attrs={'class':'name'}).text.strip()
                preco = produto.find('p',attrs={'class':'current'}).text.strip().lower().replace('kz','').strip('.')

                #Agora vamos adicionar os dados em um ficheiro CSV, criado anterirormente.
                add_csv(file=ficheiro,a=marca,b=descricao,c=tipo, d=preco)


# Vamos chamar a função para adicionar o cabeçario
#head_csv()

# Aqui vamos criar um while para repetir e chamar a função a cada 24 hora
while True:
    pegar_dados()
    time.sleep(86400)