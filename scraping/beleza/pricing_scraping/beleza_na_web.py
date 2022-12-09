from email.mime import base
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import art
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep


ascii = art.text2art("Kami Pricing")
print(ascii)
print("\033[1;33;40mForme preços competitivos na plataforma Beleza na Web\033[0;37;40m" + "\n")
# start = input("Pressione qualquer tecla para iniciar o scraping: ")

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

def scraping() :
    file = pd.read_excel(r"/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/pricing_scraping/SkuHairPro.xlsx", sheet_name="testes")
    file['sku_beleza'].unique()
    url = file['urls']
    sellers_df_list = []
    
    hairpro_df_list = []        

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

            sellers_row = [ row['sku'],  row['brand'],  row['category'], row['name'],
                        row['price'], row['seller']['name']]

            
            sellers_df_list.append(sellers_row)
            #hairpro_df_list.append(sellers_row)           

    columns_all_seller = ["sku", "brand", "category", "product_name", "price", 
                "seller_name"]
    

    columns_hairpro = ["sku", "brand", "category", "product_name", "price", 
                "seller_name"]
    
    columns_diference = [columns_hairpro[0], columns_hairpro[1], 'category', 'product_name', columns_hairpro[4], 
                        'competitor_price', 'seller_name' ]         
    
    columns_result = ['sku', 'sku_parent', 'name (*)', 'quantity (*)', 'price (*)', 'special_price', 'description',
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

    # criando planilha com diferença entre os preços
    difference_price_df = pd.DataFrame(hairpro_df, columns=columns_diference)


    # criando planilha de resultados
    products = pd.read_excel('scraping/beleza/pricing_scraping/products.xlsx')
    result_df = pd.DataFrame(columns=columns_result)
    result_df.unstack()
    
    for i in products:
        result_df['sku'] = products['sku (*)']
        result_df['sku_parent'] = products['sku_parent']
        result_df['quantity (*)'] = products['quantity (*)']
        result_df['price (*)'] = products['price (*)']
        result_df['special_price'] = products['special_price']
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

            
    # usando o ExcelWriter para escrever em um arquivo .xlsx
    writer = pd.ExcelWriter('pricing.xlsx', engine='openpyxl', )

    # armazena cada dataframe em uma planilha diferente
    all_sellers_df.to_excel(writer, sheet_name='all_sellers', index=False)      
    hairpro_df.to_excel(writer, sheet_name='hairpro', index=False)
    difference_price_df.to_excel(writer, sheet_name='difference_price', index=False)
    result_df.to_excel(writer, sheet_name='result', index=False)
    

    # salva o arquivo
    writer.close()

def send_email():

    # abre o arquivo .xlsx gerado e abre em formato binário
    pricing_report_path = r'pricing.xlsx'
    pricing_report = open(pricing_report_path, 'rb')
    
    # lê o arquivo em formato binário e codifica em base64 para anexar ao email
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(pricing_report.read())
    encoders.encode_base64(att)

    # define o cabeçalho no tipo anexo de email
    att.add_header('Content-Disposition', f'attachment', filename='pricing.xlsx')
    pricing_report.close()
    
    # define o corpo do email
    email_body = """
    
    <p>Olá! Em anexo, planilha criada pelo Pricing Scraping 
    para formação de preços dentro do marketplace Beleza na Web.
    </p>
    </br>
    <p>Atenciosamente,</p>
    <p>Equipe de Tecnologia Kami CO.</p>
    """
    emails = ['marcos@kamico.com.br']
    
    
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
    

scraping()      
send_email()    








             


        
                
            

        








