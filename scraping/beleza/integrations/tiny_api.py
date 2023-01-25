import requests
import os 
import json
import pandas as pd

class TinyApi:
            

    def get_products(self):
        file = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/planilha_mergeada.xlsx')
        sku = file['sku_kami']

        for i in sku:        
            url = f'https://api.tiny.com.br/api2/produto.obter.estoque.php'
            print(i)
            
            payload = {
                'token': '18cd84455323e7b63c4b4b9b887278c3f0efe276',
                'id': f'{i}',
                'formato': 'JSON'
            }            
            response = requests.get(url=url, params=payload)
            print(response.json())


    

if __name__ == '__main__':
    app = TinyApi() 
    app.get_products() 