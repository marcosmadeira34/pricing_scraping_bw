import requests
import json
import os
import pandas as pd


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
            'grant_type': self.grant_type
        }

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
        
        
    # Create or Update a Sku Simple or With Variation

    def create_products(self, token):
        file = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/integrations/pricing.xlsx', 
        sheet_name='hairpro')
        
        sku_id = file['sku']
        for i in range(len(sku_id)):
            
            url = f'https://api.plugg.to/skus/{sku_id[i]}' 
            
            headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json',
                'Content-Type': 'application/json',
                    }
            
            payload = {
                    "sku": str(sku_id[i]),
                    "ean": None,
                    "ncm": None,
                    "cest": None,  
                    "name":str(file['product_name'][i]),
                    "external": None,
                    "quantity": None,
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


if __name__ == '__main__':
    pluggto = PluggTo(
        client_id=os.getenv('PLUGGTO_CLIENT_ID'),
        client_secret=os.getenv('PLUGGTO_CLIENT_SECRET'),
        username=os.getenv('PLUGGTO_API_USERNAME'),
        password=os.getenv('PLUGGTO_API_SECRET'),
        grant_type = 'password'    
    )
    token_plugg = ''
    token = pluggto.get_token_by_password()
    #print(token)
    # refresh_token = pluggto.get_refresh_token(token)
    # print(refresh_token)
    create_product = pluggto.create_products(token_plugg)





