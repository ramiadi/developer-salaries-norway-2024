# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt

file_path = "salaries.csv"

try:
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Read header row
        header = next(csv_reader)
        print("Header: ", header)
        
        # Find the indexes for the columns
        erfaring_index = header.index("erfaring")
        
        # Go over each row in the CSV file
        for row in csv_reader:
            erfaring = row[erfaring_index]
            print(erfaring)

except FileNotFoundError:
    print(f"Error: The file '{file_path} was not found")
except Exception as e:
    print(f"An error occured. Please try later: {e}")

