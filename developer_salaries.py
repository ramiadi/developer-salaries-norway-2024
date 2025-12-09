from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd

csv_data = pd.read_csv('salaries.csv', delimiter=',', encoding='utf-8')
geo_data = gpd.read_file('C:/Users/ramin/Github/developer-salaries-norway-2024/shapefile/geoBoundaries-NOR-ADM1.geojson')

print("GeoJson kolonner:", geo_data.columns.tolist())