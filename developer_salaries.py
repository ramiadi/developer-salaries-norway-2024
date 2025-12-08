from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd

# 1. LAST INN DINE DATA (erstatt px.data.election())
df = pd.read_csv('salaries.csv', delimiter=',', encoding='utf-8')

