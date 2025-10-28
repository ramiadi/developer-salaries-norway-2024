# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt
import plotly.express as px

file_path = "salaries.csv"

try:
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Read header row
        header = next(csv_reader)
        # print("Header: ", header)
        
        # Find the indexes for the columns
        kjønn_index = header.index("kjønn")
        utdanning_index = header.index("utdanning")
        erfaring_index = header.index("erfaring")
        arbeidssted_index = header.index("arbeidssted")
        arbeidssituasjon_index = header.index("arbeidssituasjon")
        fag_index = header.index("fag")
        lønn_index = header.index("lønn")
        bonus_index = header.index("bonus?")
        
       
        # Hjelpevariabler
        arbeid_og_lønn = []
        lønn_per_sektor = {}
      
        # Go over each row in the CSV file
        for row in csv_reader:
            arbeidssituasjon = row[arbeidssituasjon_index].lower()
            lønn_str = row[lønn_index].strip()
            
            if lønn_str == "": continue
            lønn = int(lønn_str)
            
            arbeid_og_lønn.append([arbeidssituasjon, lønn])
        
        print("Antall gyldige rader (med lønn): ", len(arbeid_og_lønn))

        for arbeidssituasjon, lønn in arbeid_og_lønn:
            if arbeidssituasjon not in lønn_per_sektor:
                lønn_per_sektor[arbeidssituasjon] = []
                
            lønn_per_sektor[arbeidssituasjon].append(lønn)
            
        gjennomsnitt_per_sektor = {}
        
        for sektor, lønninger in lønn_per_sektor.items():
            gjennomsnitt = sum(lønninger) / len(lønninger)
            gjennomsnitt_per_sektor[sektor] = gjennomsnitt
        
        print("\nGjennomsnittslønn per arbeissituasjon: ")
        for sektor, gjennomsnitt in gjennomsnitt_per_sektor.items():
            print(f"{sektor.capitalize():40s} {int(gjennomsnitt)} NOK")
            
    # Gjør dataene klare
    sektorer = list(gjennomsnitt_per_sektor.keys())
    gjennomsnitt_lønn = list(gjennomsnitt_per_sektor.values())
    
    # Lag et interaktivt søylediagram
    fig = px.bar(
        x=sektorer,
        y=gjennomsnitt_lønn,
        color=sektorer,
        text=[f"{v:,.0f} NOK" for v in gjennomsnitt_lønn],
        title="Gjennomsnittslønn per arbeidssituasjon – Norge 2024",
        labels={"x": "Arbeidssituasjon", "y": "Gjennomsnittlig lønn (NOK)"}
    )
    
    # Designjusteringer
    fig.update_traces(textposition="outside", hovertemplate="%{x}<br>%{y:,.0f} NOK")
    fig.update_layout(
        xaxis_tickangle=-15,
        showlegend=False,
        title_font=dict(size=20, family="Arial", color="black"),
        font=dict(size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=60, l=50, r=50)
    )
    
    # Vis interaktiv graf
    fig.show()
    
    fig.write_html("salary_by_sector_interactive.html")


        
except FileNotFoundError:
    print(f"Error: The file '{file_path} was not found")
except Exception as e:
    print(f"An error occured. Please try later: {e}")

