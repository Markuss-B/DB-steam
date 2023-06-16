import pandas as pd
import random
from datetime import datetime
import ast

def generate_random_version():
    # Most of the time, return '1.0.0'
    if random.random() < 0.6:  # 90% of the time
        return '1.0.0'
    else:  # 10% of the time, generate a random version
        major = random.randint(0, 3)
        minor = random.randint(0, 9)
        patch = random.randint(0, 9)
        return f'{major}.{minor}.{patch}'



# Read the merged data
merged_data = pd.read_csv('merged_steam_data.csv')

# Initialize a list to store the SQL statements
insert_statements = []

statement = f"INSERT INTO Spēle (Nosaukums, Versija, Cena, Akcija, IzdošanasDatums, Izstrādātājs, Izplatītājs) VALUES "
insert_statements.append(statement)
# Iterate through the DataFrame rows
for index, row in merged_data.iterrows():
# Prepare the values
    steam_appid = row['steam_appid']
    name = row['name'].replace("'", "''")
    version = generate_random_version()  # Generate a random version
    price = row['price']
    price = price / 100
    discount = row['discount'] if pd.notnull(row['discount']) else '0'
    if pd.isna(row['release_date']):
        release_date = 'NULL'
    else:
        release_date_dict = ast.literal_eval(row['release_date'])
        release_date_string = release_date_dict.get('date', '')
        if release_date_string:
            try:
                release_date_object = datetime.strptime(release_date_string, '%d %b, %Y')
            except ValueError:
                release_date_object = datetime.strptime(release_date_string, '%b %d, %Y')
            release_date = release_date_object.strftime('%Y-%m-%d')
            release_date = f"'{release_date}'"
        else:
            release_date = 'NULL'
    developer = row['developer'].split(',')[0].replace("'", "''")
    publisher = row['publisher'].split(',')[0].replace("'", "''")


    # Prepare the INSERT statement
    statement = f"\t('{name}', '{version}', {price}, {discount}, {release_date}, '{developer}', '{publisher}'),"
    
    # Add the statement to the list
    insert_statements.append(statement)

insert_statements[-1] = insert_statements[-1][:-1] + ';'

# Write the statements to a file
with open('game_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
