from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd

df = pd.read_csv('salaries.csv', delimiter=',', encoding='utf-8')

fylker = gpd.read_file(r'C:\Users\ramin\Github\developer-salaries-norway-2024\shapefile\gadm41_NOR_1.shp')
fylker.plot(cmp = 'jet', edgecolor = 'black', column = 'fylker')