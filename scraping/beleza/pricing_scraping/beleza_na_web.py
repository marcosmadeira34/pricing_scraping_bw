import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import art
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from functools import lru_cache
import time
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


# importar a classe PluggTo com absolut path
start = time.time()

ascii = art.text2art("Kami Pricing")
print(ascii)
print("\033[1;33;40mForme preços competitivos na plataforma Beleza na Web\033[0;37;40m" + "\n")
# start = input("Pressione qualquer tecla para iniciar o scraping: ")

# integração com a API da PluggTo
try:
    
    from bs4 import BeautifulSoup   

except:
    
    upgrade_pip = lambda: os.system('pip3 install --upgrade pip')
    install_bs4 = lambda: os.system('pip3 install bs4')
    install_pandas = lambda: os.system('pip3 install pandas')
    install_requests = lambda: os.system('pip3 install requests')
    install_openpyxl = lambda: os.system('pip3 install openpyxl')
    install_time = lambda: os.system('pip3 install time')
    install_json = lambda: os.system('pip3 install json')
    install_datetime = lambda: os.system('pip3 install datetime')
    install_os = lambda: os.system('pip3 install os')

    up = print("Upgrading Pip")    
    print("----------------------------------------------------------")
    upgrade_pip()
    print("Downloading Bs4 Library an BeautifulSoup class ")
    print("----------------------------------------------------------")
    install_bs4()
    print("Instalation Pandas Library")
    print("----------------------------------------------------------")
    install_pandas()
    print("Instalation Requests Library")
    install_requests()
    print("Instalation Openpyxl Library")
    install_openpyxl()
    print("Instalation Time Library")
    install_time()
    print("Instalation Json Library")
    install_json()
    print("Instalation Datetime Library")
    install_datetime()
    print("Instalation OS Library")
    install_os()
    print("----------------------------------------------------------")
    print("\033[1;33;40mInstalation Complete\033[0;37;40m")


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
        self.token = response.json()['access_token']
        #return response.json()['access_token']


    @lru_cache(maxsize=None)
    def scraping(self,):
        file = pd.read_excel(r"/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/pricing_scraping/SkuHairPro23.xlsx", 
        sheet_name="truss")
        token = self.token
        
        file['sku_beleza'].unique()
        url = file['urls']
        

        sellers_df_list = []    
        for i in url:
            search = requests.get(i, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(search.content, 'html.parser')        
            id_sellers = soup.find_all('a', class_='btn btn-primary btn-block js-add-to-cart')
                    
            for id_seller in id_sellers:           
                sellers = id_seller.get('data-sku')            
                row = json.loads(sellers)[0]
                "\n"          
                
                print(
                    f"Extaindo dados do vendedor Id: {row['seller']['id']} \
                        | Loja: {row['seller']['name']} ") 
                                

                sellers_row = [row['sku'],  row['brand'],  row['category'], row['name'],
                            row['price'], row['seller']['name']]

                
                sellers_df_list.append(sellers_row)
                #hairpro_df_list.append(sellers_row)
        
        # encontrar os skus beleza na web na planilha SKUs HairPro 2112.xlsx            
        sku_sellers = pd.read_excel(
            '/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/pricing_scraping/SKUs HairPro 2112.xlsx',
            usecols=['SKU Seller', 'SKU Beleza'])

        columns_all_seller = ["sku", "brand", "category", "product_name", "price", "seller_name"]
        
        columns_except_hairpro = ["sku", "brand", "category", "product_name", "price", "seller_name"]

        columns_hairpro = ["sku", "brand", "category", "product_name", "price", "seller_name"]
                
        columns_diference = [columns_hairpro[0], columns_hairpro[1], 'category', 'product_name', columns_hairpro[4], 
                            'competitor_price', 'difference_price', 'suggest_price', 'ganho_%']

        # columns_suggest_price = [columns_diference[]]    
        columns_result = ['sku','sku (*)', 'sku_parent', 'name (*)', 'quantity (*)', 'price (*)', 'special_price', 'description',
                        'brand', 'link', 'warranty_time', 'warranty_message', 'length', 'width', 'height', 'weight',
                        'ean', 'isbn', 'ncm', 'nbm', 'link_image_1', 'link_image_2', 'link_image_3', 'link_image_4',
                        'link_image_5', 'link_image_6', 'link_image_7', 'link_image_8', 'link_image_9', 'link_image_10',
                        'attribute_name_1', 'attribute_value_1', 'attribute_name_2', 'attribute_value_2', 'attribute_name_3',
                        'attribute_value_3', 'attribute_name_4', 'attribute_value_4', 'attribute_name_5', 'attribute_value_5',
                        'attribute_name_6', 'attribute_value_6', 'attribute_name_7', 'attribute_value_7', 'attribute_name_8',
                        'attribute_value_8', 'attribute_name_9', 'attribute_value_9', 'attribute_name_10', 'attribute_value_10',
                        'attribute_name_11', 'attribute_value_11', 'attribute_name_12', 'attribute_value_12', 'attribute_name_13',
                        'attribute_value_13', 'attribute_name_14', 'attribute_value_14', 'attribute_name_15', 'attribute_value_15',
                        'attribute_name_16', 'attribute_value_16', 'attribute_name_17', 'attribute_value_17', 'attribute_name_18',
                        'attribute_value_18', 'attribute_name_19', 'attribute_value_19', 'attribute_name_20', 'attribute_value_20',
                        'attribute_name_21', 'attribute_value_21', 'attribute_name_22', 'attribute_value_22', 'attribute_name_23',
                        'attribute_value_23', 'attribute_name_24', 'attribute_value_24', 'attribute_name_25', 'attribute_value_25',
                        'attribute_name_26', 'attribute_value_26', 'attribute_name_27', 'attribute_value_27', 'attribute_name_28',
                        'attribute_value_28', 'attribute_name_29', 'attribute_value_29', 'attribute_name_30', 'attribute_value_30',
                        'full_category_tree_1 (ie: base > cat > subcat > subsubcat)', 'full_category_tree_2 (ie: base > cat > subcat > subsubcat)',
                        'full_category_tree_3 (ie: base > cat > subcat > subsubcat)', 'handling_time', 'manufacture_time', 'model',
                        'cest', 'location', 'ean_not_mandatory', 'cost', 'origin', 'marketplaces_available', ]


        # criando DataFrame com todos os dados extraidos	       
        all_sellers_df = pd.DataFrame(sellers_df_list, columns=columns_all_seller)
        all_sellers_df.drop_duplicates(keep='first', inplace=True)


        # filtrar os dados para apenas do vendedor HairPro
        seller_name = all_sellers_df.groupby('seller_name')   
        hairpro_filter_hairpro = seller_name.get_group('HAIRPRO')   
        hairpro_df = pd.DataFrame(hairpro_filter_hairpro, columns=columns_hairpro)

        
        # todos os vendedores menos o HairPro
        except_hairpro_df = all_sellers_df.drop(all_sellers_df[all_sellers_df['seller_name'].str.contains('HAIRPRO')].index)
        except_hairpro_df = pd.DataFrame(except_hairpro_df,  columns=columns_except_hairpro)
        except_hairpro_df.drop_duplicates(subset='sku', keep='first', inplace=True)

        # criando planilha com diferença entre os preços
        difference_price_df = pd.DataFrame(hairpro_df, columns=columns_diference)

        
        # comparar os precos Hairpro com os precos dos except_hairpro_df
        for i in hairpro_df['sku']:
            for j in except_hairpro_df['sku']:
                if i == j:
                    difference_price_df.loc[difference_price_df['sku'] == i, 'competitor_price'] = except_hairpro_df.loc[except_hairpro_df['sku'] == j, 'price'].values[0]
                    difference_price_df['difference_price'] = difference_price_df['competitor_price'] - difference_price_df['price'] - 0.10
                    difference_price_df['difference_price'] = difference_price_df['difference_price'].round(6)
                
                # quando difference_price_df['competitor_price'] for zero e sua serie for ambigua, sugerir um preco de 10% maior    
                # e arrendondar para 2 casas decimais o preco sugerido
                if difference_price_df['competitor_price'].isnull().values.any():
                    difference_price_df['suggest_price'] = difference_price_df['price'].round(6)
                
                
                # quando o preço da Hairpro for maior que o preço do concorrente, sugerir o preço de 0,10 centavos a menos
                # que o preço do concorrente e arrendondar para 2 casas decimais o preco sugerido            
                if difference_price_df['price'].min() < difference_price_df['competitor_price'].max():
                    difference_price_df['suggest_price'] = difference_price_df['competitor_price'].round(6) - 0.10

                
                # percentual de diferença entre o preço da Hairpro e o preço do concorrente
                difference_price_df['ganho_%'] = (difference_price_df['suggest_price'] / difference_price_df['price']) -1
                difference_price_df['ganho_%'] = difference_price_df['ganho_%'].round(2) * 100
                
        # criando planilha de resultados
        products = pd.read_excel('/home/marcosmadeira/src/PricingScraping_2.0/scraping/products.xlsx')   
        
        result_df = pd.DataFrame(columns=columns_result)

        plan_base = pd.read_excel("/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/pricing_scraping/SKUs HairPro 2112.xlsx", 
                                    usecols=['SKU Seller', 'SKU Beleza'])
        plan_base.rename(columns = {'SKU Beleza' : 'sku_beleza', 'SKU Seller' : 'sku_kami'}, inplace=True)
            

        # <---Start chamando API PluggTo recebe valores de estoque --->
        """ file = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/products.xlsx')
        sku = file['sku (*)']

        pluggto_stock = []
        for i in sku:
            url = f'https://api.plugg.to/skus/{i}'
            headers = {
                'Authorization': f'Bearer {token} ',
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

            else:
                print(f'Produto {i} não encontrado. Token expirado.') """

        # <---End chamando API PluggTo recebe valores de estoque --->   
        

        # iterando sobre a planilha de produtos para copiar os valores para a planilha de resultados        
        for i in products:
            result_df['sku'] = products['sku (*)']
            result_df['sku_parent'] = products['sku_parent']
            result_df['quantity (*)'] = products['quantity (*)']
            result_df['price (*)'] = products['price (*)']
            result_df['description'] = products['description']
            result_df['brand'] = products['brand']
            result_df['link'] = products['link']
            result_df['warranty_time'] = products['warranty_time']
            result_df['warranty_message'] = products['warranty_message']
            result_df['length'] = products['length']
            result_df['width'] = products['width']
            result_df['height'] = products['height']
            result_df['weight'] = products['weight']
            result_df['ean'] = products['ean']
            result_df['isbn'] = products['isbn']
            result_df['ncm'] = products['ncm']
            result_df['nbm'] = products['nbm']
            result_df['link_image_1'] = products['link_image_1']
            result_df['link_image_2'] = products['link_image_2']
            result_df['link_image_3'] = products['link_image_3']
            result_df['link_image_4'] = products['link_image_4']
            result_df['link_image_5'] = products['link_image_5']
            result_df['link_image_6'] = products['link_image_6']
            result_df['link_image_7'] = products['link_image_7']
            result_df['link_image_8'] = products['link_image_8']
            result_df['link_image_9'] = products['link_image_9']
            result_df['link_image_10'] = products['link_image_10']
            result_df['attribute_name_1'] = products['attribute_name_1']
            result_df['attribute_value_1'] = products['attribute_value_1']
            result_df['attribute_name_2'] = products['attribute_name_2']
            result_df['attribute_value_2'] = products['attribute_value_2']
            result_df['attribute_name_3'] = products['attribute_name_3']
            result_df['attribute_value_3'] = products['attribute_value_3']
            result_df['attribute_name_4'] = products['attribute_name_4']
            result_df['attribute_value_4'] = products['attribute_value_4']
            result_df['attribute_name_5'] = products['attribute_name_5']
            result_df['attribute_value_5'] = products['attribute_value_5']
            result_df['attribute_name_6'] = products['attribute_name_6']
            result_df['attribute_value_6'] = products['attribute_value_6']
            result_df['attribute_name_7'] = products['attribute_name_7']
            result_df['attribute_value_7'] = products['attribute_value_7']
            result_df['attribute_name_8'] = products['attribute_name_8']
            result_df['attribute_value_8'] = products['attribute_value_8']
            result_df['attribute_name_9'] = products['attribute_name_9']
            result_df['attribute_value_9'] = products['attribute_value_9']
            result_df['attribute_name_10'] = products['attribute_name_10']
            result_df['attribute_value_10'] = products['attribute_value_10']
            result_df['attribute_name_11'] = products['attribute_name_11']
            result_df['attribute_value_11'] = products['attribute_value_11']
            result_df['attribute_name_12'] = products['attribute_name_12']
            result_df['attribute_value_12'] = products['attribute_value_12']
            result_df['attribute_name_13'] = products['attribute_name_13']
            result_df['attribute_value_13'] = products['attribute_value_13']
            result_df['attribute_name_14'] = products['attribute_name_14']  
            result_df['attribute_value_14'] = products['attribute_value_14']
            result_df['attribute_name_15'] = products['attribute_name_15']
            result_df['attribute_value_15'] = products['attribute_value_15']
            result_df['attribute_name_16'] = products['attribute_name_16']
            result_df['attribute_value_16'] = products['attribute_value_16']
            result_df['attribute_name_17'] = products['attribute_name_17']
            result_df['attribute_value_17'] = products['attribute_value_17']
            result_df['attribute_name_18'] = products['attribute_name_18']
            result_df['attribute_value_18'] = products['attribute_value_18']
            result_df['attribute_name_19'] = products['attribute_name_19']
            result_df['attribute_value_19'] = products['attribute_value_19']
            result_df['attribute_name_20'] = products['attribute_name_20']
            result_df['attribute_value_20'] = products['attribute_value_20']
            result_df['attribute_name_21'] = products['attribute_name_21']
            result_df['attribute_value_21'] = products['attribute_value_21']
            result_df['attribute_name_22'] = products['attribute_name_22']
            result_df['attribute_value_22'] = products['attribute_value_22']
            result_df['attribute_name_23'] = products['attribute_name_23']
            result_df['attribute_value_23'] = products['attribute_value_23']
            result_df['attribute_name_24'] = products['attribute_name_24']
            result_df['attribute_value_24'] = products['attribute_value_24']
            result_df['attribute_name_25'] = products['attribute_name_25']
            result_df['attribute_value_25'] = products['attribute_value_25']
            result_df['attribute_name_26'] = products['attribute_name_26']
            result_df['attribute_value_26'] = products['attribute_value_26']
            result_df['attribute_name_27'] = products['attribute_name_27']
            result_df['attribute_value_27'] = products['attribute_value_27']
            result_df['attribute_name_28'] = products['attribute_name_28']
            result_df['attribute_value_28'] = products['attribute_value_28']
            result_df['attribute_name_29'] = products['attribute_name_29']
            result_df['attribute_value_29'] = products['attribute_value_29']
            result_df['attribute_name_30'] = products['attribute_name_30']
            result_df['attribute_value_30'] = products['attribute_value_30']
            result_df['full_category_tree_1 (ie: base > cat > subcat > subsubcat)'] = products['full_category_tree_1 (ie: base > cat > subcat > subsubcat)']
            result_df['full_category_tree_2 (ie: base > cat > subcat > subsubcat)'] = products['full_category_tree_2 (ie: base > cat > subcat > subsubcat)']
            result_df['full_category_tree_3 (ie: base > cat > subcat > subsubcat)'] = products['full_category_tree_3 (ie: base > cat > subcat > subsubcat)']
            result_df['handling_time'] = products['handling_time']
            result_df['manufacture_time'] = products['manufacture_time']
            result_df['model'] = products['model']
            result_df['cest'] = products['cest']
            result_df['location'] = products['location']
            result_df['ean_not_mandatory'] = products['ean_not_mandatory']
            result_df['cost'] = products['cost']
            result_df['origin'] = products['origin']
            result_df['marketplaces_available'] = products['marketplaces_available']      

            if result_df['sku'].isin(products['sku (*)']).any():
                result_df['special_price'] = difference_price_df['suggest_price']
                result_df['special_price'] = result_df['special_price'].round(6)
        
        # adicionando valores da coluna 'quantity' do dataframe 'pluggto_df' ao dataframe 'result_df'
        """ for i in pluggto_df['sku']:
            result_df['quantity (*)'] = pluggto_df[' '] """
        
        # usando o ExcelWriter para escrever em um arquivo .xlsx
        writer = pd.ExcelWriter('/home/marcosmadeira/src/PricingScraping_2.0/scraping/pricing.xlsx', engine='openpyxl', )
        
        # armazena cada dataframe em uma planilha diferente
        all_sellers_df.to_excel(writer, sheet_name='all_sellers', index=False)      
        hairpro_df.to_excel(writer, sheet_name='hairpro', index=False)
        difference_price_df.to_excel(writer, sheet_name='difference_price', index=False)
        result_df.to_excel(writer, sheet_name='result', index=False)
        except_hairpro_df.to_excel(writer, sheet_name='except_hairpro', index=False)
        
        # salva o arquivo
        writer.close()
        
        # abre o arquivo pricing.xlsx e renomeia colunas
        plan_pricing_result = pd.read_excel('/home/marcosmadeira/src/PricingScraping_2.0/scraping/pricing.xlsx', sheet_name="result")
        plan_pricing_result.rename(columns = {'sku' : 'sku_kami'}, inplace=True)
        plan_pricing_result.rename(columns = {'sku (*)' : 'sku_beleza'}, inplace=True)

        
        # realiza o merge entre os dois arquivos, exclui o sku_beleza_y e renomeia o sku_beleza_x
        plan_result = pd.merge(plan_base,plan_pricing_result, on="sku_kami", how='left')
        plan_result.drop(['sku_beleza_y'], axis=1, inplace=True)
        plan_result.rename(columns = {'sku_beleza_x' : 'sku_beleza'}, inplace= True)

        
        # reordena as colunas
        plan_result = plan_result[['sku_beleza','sku_kami','sku_parent', 'name (*)', 'quantity (*)', 'price (*)', 
        'special_price', 'description', 'brand', 'link', 'warranty_time', 'warranty_message', 'length',
        'width', 'height', 'weight', 'ean', 'isbn', 'ncm', 'nbm', 'link_image_1', 'link_image_2',
        'link_image_3', 'link_image_4', 'link_image_5', 'link_image_6', 'link_image_7', 'link_image_8',
        'link_image_9', 'link_image_10', 'attribute_name_1', 'attribute_value_1', 'attribute_name_2',
        'attribute_value_2', 'attribute_name_3', 'attribute_value_3', 'attribute_name_4', 'attribute_value_4',
        'attribute_name_5', 'attribute_value_5', 'attribute_name_6', 'attribute_value_6', 'attribute_name_7',
        'attribute_value_7', 'attribute_name_8', 'attribute_value_8', 'attribute_name_9', 'attribute_value_9',
        'attribute_name_10', 'attribute_value_10', 'attribute_name_11', 'attribute_value_11', 'attribute_name_12',
        'attribute_value_12', 'attribute_name_13', 'attribute_value_13', 'attribute_name_14', 'attribute_value_14',
        'attribute_name_15', 'attribute_value_15', 'attribute_name_16', 'attribute_value_16', 'attribute_name_17',
        'attribute_value_17', 'attribute_name_18', 'attribute_value_18', 'attribute_name_19', 'attribute_value_19',
        'attribute_name_20', 'attribute_value_20', 'attribute_name_21', 'attribute_value_21', 'attribute_name_22',
        'attribute_value_22', 'attribute_name_23', 'attribute_value_23', 'attribute_name_24', 'attribute_value_24',
        'attribute_name_25', 'attribute_value_25', 'attribute_name_26', 'attribute_value_26', 'attribute_name_27',
        'attribute_value_27', 'attribute_name_28', 'attribute_value_28', 'attribute_name_29', 'attribute_value_29',
        'attribute_name_30', 'attribute_value_30', 'full_category_tree_1 (ie: base > cat > subcat > subsubcat)', 
        'full_category_tree_2 (ie: base > cat > subcat > subsubcat)', 'full_category_tree_3 (ie: base > cat > subcat > subsubcat)', 
        'handling_time', 'manufacture_time', 'model', 'cest', 'location', 'ean_not_mandatory',
        'cost', 'origin', 'marketplaces_available' ]]

        
        # abre o arquivo princing,xlsx na aba difference_price e renomeia as colunas
        suggest_price = pd.read_excel('/home/marcosmadeira/src/PricingScraping_2.0/scraping/pricing.xlsx',
                                        sheet_name='difference_price', engine='openpyxl')                    
        suggest_price.rename(columns = {'sku': 'sku_beleza'}, inplace=True)
        suggest_price = suggest_price[['sku_beleza', 'suggest_price']]
        
        
        # converte o tipo de dado para string    
        suggest_price['sku_beleza'] = suggest_price['sku_beleza'].astype(str)
        print(type(suggest_price['sku_beleza'][0]))
        

        # merge entre as planilhas
        plan_result_price = pd.merge(plan_result, suggest_price, on="sku_beleza", how="left")

        # converte o tipo de dado para float
        plan_result_price['suggest_price'] = plan_result_price['suggest_price'].astype(float)                           
        plan_result_price.drop(['special_price'], axis=1, inplace=True)
        plan_result_price.rename(columns = {'suggest_price' : 'special_price'}, inplace= True)

        # exclui linhas com quantity (*) nulos
        #plan_result_price.dropna(subset=['quantity (*)'], inplace=True)
        
        # exclui linhas com special_price nulos
        plan_result_price.dropna(subset=['special_price'], inplace=True)
        plan_result_price.dropna(subset=['description'], inplace=True)    

        # excluindo coluna sku_beleza
        plan_result_price.drop(['sku_beleza'], axis=1, inplace=True)

        # renomeia coluna sku_kami 
        plan_result_price.rename(columns = {'sku_kami' : 'sku (*)'}, inplace= True)

        plan_result_price = plan_result_price[['sku (*)', 'sku_parent', 'name (*)', 'quantity (*)', 'price (*)', 
        'special_price', 'description', 'brand', 'link', 'warranty_time', 'warranty_message', 'length',
        'width', 'height', 'weight', 'ean', 'isbn', 'ncm', 'nbm', 'link_image_1', 'link_image_2',
        'link_image_3', 'link_image_4', 'link_image_5', 'link_image_6', 'link_image_7', 'link_image_8',
        'link_image_9', 'link_image_10', 'attribute_name_1', 'attribute_value_1', 'attribute_name_2',
        'attribute_value_2', 'attribute_name_3', 'attribute_value_3', 'attribute_name_4', 'attribute_value_4',
        'attribute_name_5', 'attribute_value_5', 'attribute_name_6', 'attribute_value_6', 'attribute_name_7',
        'attribute_value_7', 'attribute_name_8', 'attribute_value_8', 'attribute_name_9', 'attribute_value_9',
        'attribute_name_10', 'attribute_value_10', 'attribute_name_11', 'attribute_value_11', 'attribute_name_12',
        'attribute_value_12', 'attribute_name_13', 'attribute_value_13', 'attribute_name_14', 'attribute_value_14',
        'attribute_name_15', 'attribute_value_15', 'attribute_name_16', 'attribute_value_16', 'attribute_name_17',
        'attribute_value_17', 'attribute_name_18', 'attribute_value_18', 'attribute_name_19', 'attribute_value_19',
        'attribute_name_20', 'attribute_value_20', 'attribute_name_21', 'attribute_value_21', 'attribute_name_22',
        'attribute_value_22', 'attribute_name_23', 'attribute_value_23', 'attribute_name_24', 'attribute_value_24',
        'attribute_name_25', 'attribute_value_25', 'attribute_name_26', 'attribute_value_26', 'attribute_name_27',
        'attribute_value_27', 'attribute_name_28', 'attribute_value_28', 'attribute_name_29', 'attribute_value_29',
        'attribute_name_30', 'attribute_value_30', 'full_category_tree_1 (ie: base > cat > subcat > subsubcat)', 
        'full_category_tree_2 (ie: base > cat > subcat > subsubcat)', 'full_category_tree_3 (ie: base > cat > subcat > subsubcat)', 
        'handling_time', 'manufacture_time', 'model', 'cest', 'location', 'ean_not_mandatory',
        'cost', 'origin', 'marketplaces_available']]

        #plan_result_price = plan_result_price.loc([plan_result_price['special_price'] > 0])
        plan_result_price.to_excel('/home/marcosmadeira/src/PricingScraping_2.0/scraping/pricing_version_2_0.xlsx', 
                                    engine='openpyxl', index=False)


    @lru_cache(maxsize=None)
    def send_email(self):

        # abre o arquivo .xlsx gerado e abre em formato binário
        pricing_report_path = r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/pricing_version_2_0.xlsx'
        pricing_report = open(pricing_report_path, 'rb')
        
        # lê o arquivo em formato binário e codifica em base64 para anexar ao email
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(pricing_report.read())
        encoders.encode_base64(att)

        # define o cabeçalho no tipo anexo de email
        att.add_header('Content-Disposition', f'attachment', filename=('pricing_version_2_0.xlsx'))
        pricing_report.close()
        
        # define o corpo do email
        email_body = """
        
        <p>Teste .... Olá! Em anexo, planilha criada pelo Pricing Scraping 
        para formação de preços dentro do marketplace Beleza na Web.
        </p>
        </br>
        <p>Atenciosamente,</p>
        <p>Equipe de Tecnologia Kami CO.</p>
        """
        emails = ['marcos@kamico.com.br', 'bruno.oliveira@kamico.com.br']

        
        for email in emails:
        # define o email de origem e destino
            msg = MIMEMultipart()
            msg["Subject"] = "Pricing Scraping - Beleza na Web"
            msg["From"] = "dev@kamico.com.br"
            msg["To"] = email
            password = "Kami@2022Dev"
            msg.attach(MIMEText(email_body, 'html'))
            msg.attach(att)  
            msg.add_header('Content-Type', 'text/html')
            
            # define o servidor de email e a porta
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            s.login(msg["From"], password)
            s.sendmail(msg["From"], msg["To"], msg.as_string().encode('utf-8'))
            s.quit()
            print(f'Email enviado com sucesso para {email}')
            
        #pegar a coluna price e retornar o menor numero para cada produto do concorrente
        """ competing_sellers = sellers_df.groupby('sku')
        for i in competing_sellers.index:
            print(f"{i} - {competing_sellers.loc[i]['seller_name']}") 
        
        # merge dos DataFrames para comparar os preços dos produtos
        merge_df = pd.merge(competing_sellers, hairpro_df, on='sku')
        merge_df.drop([
                        'diferenca_x', 'status_x', 'preco_sugerido_x',
                        'difal_AC_x',
                        'difal_AL_x',
                        'difal_AP_x',
                        'difal_AM_x',
                        'difal_BA_x',
                        'difal_CE_x',
                        'difal_DF_x',
                        'difal_ES_x',
                        'difal_GO_x',
                        'difal_MA_x',
                        'difal_MT_x',
                        'difal_MS_x',
                        'difal_MG_x',
                        'difal_PA_x',
                        'difal_PB_x',
                        'difal_PR_x',
                        'difal_PE_x',
                        'difal_PI_x',
                        'difal_RJ_x',
                        'difal_RN_x',
                        'difal_RS_x',
                        'difal_RO_x',
                        'difal_RR_x',
                        'difal_SC_x',
                        'difal_SP_x',
                        'difal_SE_x',
                        'difal_TO_x',
                        'Pis_x',
                        'Cofins_x',
                        'IRPJ Venda Prod_x',
                        'CSLL Venda Prod_x',
                        'brand_y',
                        'category_y',
                        'difal_AC_y',
                        'difal_AL_y',
                        'difal_AP_y',
                        'difal_AM_y',
                        'difal_BA_y',
                        'difal_CE_y',
                        'difal_DF_y',
                        'difal_ES_y',
                        'difal_GO_y',
                        'difal_MA_y',
                        'difal_MT_y',
                        'difal_MS_y',
                        'difal_PA_y',
                        'difal_PB_y',
                        'difal_PR_y',
                        'difal_PE_y',
                        'difal_PI_y',
                        'difal_RJ_y',
                        'difal_RN_y',
                        'difal_RS_y',
                        'difal_RO_y',
                        'difal_RR_y',
                        'difal_SC_y',
                        'difal_SP_y',
                        'difal_SE_y',
                        'difal_TO_y',
                        'Pis_y',
                        'Cofins_y',
                        

                        
                        
                        
                        ], axis=1, inplace=True)
        
        # cálculo da diferença entre os preços dos produtos
        difference = merge_df['price_x'] - merge_df['price_y']
        merge_df['diferenca_y'] = difference


        # status de acordo com a diferença entre os preços (ganho ou perda)
        merge_df['status_y'] = merge_df['diferenca_y'].apply(lambda x: 'lider' if x >= 0 else 'perda')         

        
        if merge_df['diferenca_y'].any() == 0:
            suggest_price_lider = merge_df['price_x'].apply(lambda x: x - 0)
            merge_df['preco_sugerido_y'] == suggest_price_lider
        
        else:
            suggest_price =  merge_df['price_x'].apply(lambda x: x - 0.1) 
            merge_df['preco_sugerido_y'] = suggest_price

            # calculo difal Minas Gerais
            valor_icms_interestadual_MG = merge_df['preco_sugerido_y'].apply(lambda x: x * 0.12)
            valor_mercadoria_MG = merge_df['preco_sugerido_y'] - valor_icms_interestadual_MG
            calc_difal_MG = valor_mercadoria_MG.apply(lambda x: x / (1-0.18))
            icms_sp = calc_difal_MG.apply(lambda x: x * 0.18)
            result_difa-l_MG = icms_sp - valor_icms_interestadual_MG
            merge_df['difal_MG_y'] = result_difal_MG

            # calculo csll
            calc_csll = merge_df['preco_sugerido_y'].apply(lambda x: x * 1.08 / 100)
            merge_df['CSLL Venda Prod_y'] = calc_csll

            # calculo irpj sem adicional de imposto
            calc_irpj = merge_df['preco_sugerido_y'].apply(lambda x: x * 1.20 / 100)
            merge_df['IRPJ Venda Prod_y'] = calc_irpj 

            # comissão da plataforma       

        # sellers_df.to_excel('Pricing.xlsx', index=False)

        with open('Pricing.xlsx', 'rb') as f:
            data = f.read()  """

        print("\033[1;33;40mScraping Complete\033[0;37;40m")
        stop = time.time() - start
        print(f"Tempo de execução: {stop} segundos")    
        

if __name__ == '__main__':
    app = PluggTo(
        client_id = os.getenv('client_id'),
        client_secret = os.getenv('client_secret'),
        username = os.getenv('api_user'),
        password = os.getenv('api_secret'),
        grant_type = os.getenv('grant_type')
    )
    app.get_token_by_password()
    app.scraping()
    app.send_email()

    







             


        
                
            

        








