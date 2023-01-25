import requests
import json
import os
import pandas as pd
import dotenv
           

# Authentication by password
dotenv.load_dotenv(dotenv.find_dotenv())

class PluggTo:
    def __init__(self, client_id, client_secret, username, password, grant_type):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.grant_type = grant_type


    # Authentication by password
    def get_token_by_password(self):
        url = 'https://api.plugg.to/oauth/token'
        
        payload = {            
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
            'grant_type': self.grant_type,

       }

        headers = {            
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        
        response = requests.post(url, data=payload, headers=headers)
        print(response.text)
        print(response.status_code)
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        print(access_token)
        print(refresh_token)
        
        
    # Create or Update a Sku Simple or With Variation

    def create_products(self, token):
        file = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/integrations/planilha_mergeada.xlsx', 
        sheet_name='hairpro')
        
        sku_id = file['sku_beleza']
        for i in range(len(sku_id)):
            
            url = f'https://api.plugg.to/skus/{sku_id[i]}' 
            
            headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json',
                'Content-Type': 'application/json',
                    }
            
            payload = {
                    "sku": str(sku_id[i]),
                    "ean": str(sku_id['ean'][i]),
                    "ncm": str(sku_id['ncm'][i]),
                    "cest": None,  
                    "name":str(file['product_name'][i]),
                    "external": None,
                    "quantity": int(i['quantity'][i]),
                    "special_price": None,
                    "price": str(file['price'][i]),
                    "short_description": None,
                    "description": None,
                    "brand": None,
                    "model": None,  
                    "cost": None,
                    "warranty_time": None,
                    "warranty_message": None,
                    "link": None,     
                                
            }
            
            response = requests.put(url, data=json.dumps(payload), headers=headers)
            print(response.json())

    
    def get_products_pluggto(self):        
        file = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/products.xlsx')
        sku = file['sku (*)']

        pluggto_stock = []
        for i in sku:
            url = f'https://api.plugg.to/skus/{i}'
            
            headers = {
                'Authorization': f'Bearer d69f1c708ee20d9fada4bf1a7a0f0f2c83f9356d',
                'Accept': 'application/json',
                'Content-Type': 'application/json,'
            }

            params = {}

            pluggto_columns = ['sku', 'quantity']

            response = requests.get(url=url, headers=headers, data=json.dumps(params))
            if response.status_code == 200:
                sku_kami = response.json()['Product']['sku']
                #print(sku_kami)
                quantity = response.json()['Product']['quantity']
                #print(quantity)            
                pluggto_stock.append([sku_kami, quantity])
                print(f'Produto {sku_kami} encontrado contendo {quantity} em estoque')
        
        pluggto_df = pd.DataFrame(pluggto_stock, columns=pluggto_columns)
        pluggto_df.to_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/pluggto_stock.xlsx', index=False)




if __name__ == '__main__':
    pluggto = PluggTo(
        client_id = os.getenv('client_id'),
        client_secret = os.getenv('client_secret'),
        username = os.getenv('api_user'),
        password = os.getenv('api_secret'),
        grant_type = os.getenv('grant_type'))
    pluggto.get_token_by_password()





