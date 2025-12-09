import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, html, dcc

# ===== DATA LOADING =====
def load_data(csv_path='salaries.csv', shp_path='shapefiles/geoBoundaries-NOR-ADM1_simplified.shp'):
    csv_data = pd.read_csv(csv_path, delimiter=',', encoding='utf-8')
    geo_data = gpd.read_file(shp_path)
    return csv_data, geo_data

# ===== NORMALIZATION =====
def normalize_region_names(geo_df, csv_df):
    # Fix mis-encoded names from the shapefile
    geo_fix = {
        "MÃ¸re og Romsdal": "Møre og Romsdal",
        "TrÃ¸ndelag": "Trøndelag",
    }
    geo_df["shapeName"] = geo_df["shapeName"].replace(geo_fix)

    # Optional: fix common CSV variants to match shapefile
    csv_fix = {
        "More og Romsdal": "Møre og Romsdal",
        "Moere og Romsdal": "Møre og Romsdal",
        "Trondelag": "Trøndelag",
    }
    csv_df["arbeidssted"] = csv_df["arbeidssted"].replace(csv_fix)
    return geo_df, csv_df

# ===== CHOROPLETH =====
def build_choropleth(csv_data, geo_data):
    # Aggregate salary by region
    region_salary = (
        csv_data
        .groupby('arbeidssted', as_index=False)['lønn']
        .mean()
        .rename(columns={'arbeidssted': 'shapeName', 'lønn': 'avg_salary'})
    )

    # Merge with geo data
    geo_merged = geo_data.merge(region_salary, on='shapeName', how='left')

    # Build GeoJSON
    geojson = json.loads(geo_merged.to_json())

    # Choropleth with featureidkey (matches properties.shapeName in the GeoJSON)
    fig = px.choropleth(
        geo_merged,
        geojson=geojson,
        locations='shapeName',
        featureidkey='properties.shapeName',
        color='avg_salary',
        color_continuous_scale='Viridis',
        labels={'avg_salary': 'Snittlønn (NOK)'},
        title='Utviklerlønn i Norge',
        hover_name='shapeName',
        hover_data={'avg_salary': ':.0f'}
    )

    # Layout similar to the Plotly example
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        height=650,
    )
    return fig

# 1. Salary by Experience Level
# Bar chart showing average salary vs years of experience
# Helps show career progression
def avg_salary_and_yearly_experience_graph(csv_data, geo_data):
    exp_salary = (
        csv_data
        .groupby("erfaring", as_index=False)["lønn"]
        .mean()
        .sort_values("erfaring")
    )

    fig = px.scatter(
        exp_salary,
        x="erfaring",
        y="lønn",
        title="Gjennomsnittlig lønn etter erfaring",
        labels={"erfaring": "År erfaring", "lønn": "Snittlønn (NOK)"},
        color="lønn",
        color_continuous_scale="Viridis",
        trendline="ols",
        trendline_color_override="red",
    )
    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        title_font_size=18,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#ffffff"),
    )
    return fig

# Salary by Tech Stack (fag) - which skills pay most
def salary_tech_and_avg_salary(csv_data):
    tech_pay = (
        csv_data
        .groupby("fag", as_index=False)["lønn"]
        .mean()
        .sort_values("lønn", ascending=False)  # highest at top
    )

    fig = px.bar(
        tech_pay,
        x="lønn",
        y="fag",
        title="Gjennomsnittlig lønn i hvert fagområde",
        labels={"fag": "Fagområde", "lønn": "Snittlønn (NOK)"},
        color="lønn",
        color_continuous_scale="Plasma",
        text="lønn",
    )

    fig.update_traces(
        texttemplate="%{text:,.3s}",
        textposition="inside",
        textfont=dict(size=16),
        hovertemplate="Fag: %{y}<br>Snittlønn: %{x:,.0f} kr",
    )

    fig.update_yaxes(
        categoryorder="total descending",
        tickfont=dict(size=16, color="#ffffff"), 
    )
    fig.update_xaxes(
        tickformat="~s",
        tickfont=dict(size=14, color="#ffffff"),
        titlefont=dict(size=15, color="#ffffff"),
    )

    fig.update_layout(
        height=600,
        bargap=0.18,
        margin=dict(l=200, r=60, t=60, b=80, pad=13),
        showlegend=False,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#ffffff", size=13),
        title_font_size=22,
    )
    return fig

# ===== BUILD DASHBOARD =====
def build_dashboard(csv_data, geo_data):
    app = Dash(__name__)
    app.layout = html.Div(
        style={
            "maxWidth": "1000%",
            "margin": "0 auto"
            },
        children=[
            html.H2("Utviklerlønn i Norge"),
            dcc.Graph(id="choropleth", figure=build_choropleth(csv_data, geo_data)),
            dcc.Graph(id="experience", figure=avg_salary_and_yearly_experience_graph(csv_data, geo_data)),
            dcc.Graph(id="fag", figure=salary_tech_and_avg_salary(csv_data)),
        ]
    )
    return app

# ===== MAIN =====
if __name__ == "__main__":
    csv_data, geo_data = load_data()
    geo_data, csv_data = normalize_region_names(geo_data, csv_data)

    app = build_dashboard(csv_data, geo_data)
    app.run(debug=True)