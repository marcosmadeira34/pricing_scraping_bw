from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_excel(r'/home/marcosmadeira/src/PricingScraping_2.0/scraping/beleza/integrations/pricing.xlsx', sheet_name='hairpro')

df = pd.DataFrame(df)

fig = px.bar(df, x='sku', y='price', color='price', barmode='group', width=800, height=600)

app.layout = html.Div(children=[
        html.H1(children='PAINEL DE ACOMPANHAMENTO PRICING'),
        html.Div(children='''
            Dash: A web application framework for Python.
            '''),
        dcc.Graph(
        id='example-graph',
        figure=fig

    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
