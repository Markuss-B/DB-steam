import pandas as pd
import csv

# Read the merged data
merged_data = pd.read_csv('merged_steam_data.csv')

# Initialize a list to store the SQL statements
descs = []

# Iterate through the DataFrame rows
for index, row in merged_data.iterrows():
    name = row['name']
    desc = row['short_description']
    descs.append([name, desc])


with open('game_descs.csv', 'w', encoding='utf-8-sig', newline='') as combined_file:
    combine_writer = csv.writer(combined_file)
    combine_writer.writerow(['name', 'short_description'])
    for desc in descs:
        combine_writer.writerow(desc)

with open('game_descs_only.csv' , mode='w', encoding='utf-8-sig', newline='') as desc_file:
    desc_writer = csv.writer(desc_file)
    desc_writer.writerow(['short_description'])
    for desc in descs:
        desc_writer.writerow([desc[1]])
    

