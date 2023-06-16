import pandas as pd
import random

# Read the data
users = pd.read_csv('csv\\users.csv')

# List of category names
category_names = ['Vecie Labie', 'Adrenalīna Pumpētāji', 'Galvaslauzīšana', 'Krievu Rulete', 'Dzīvības Spēles', 'Kosmiskās Operas', 'Burvju Pasaule', 'Mierīgais Laiks', 'Neparastie Pērles', 'Komandas Cīņas', 'Pārāk Sarežģīti Man']

# Initialize a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO LietotājaKategorija VALUES"
insert_statements.append(statement)

# Function to create an INSERT statement
def create_insert_statement(lietotajs_id, nosaukums):
    statement = f"\t({lietotajs_id}, '{nosaukums}'),"
    return statement

# For each user, assign up to three random categories
for _, user in users.iterrows():
    if random.random() < 0.5:
        continue
    if len(insert_statements) >= 100:  # Limit the total inserts to 50
        break

    categories_for_this_user = random.sample(category_names, min(3, len(category_names)))

    for category in categories_for_this_user:
        if random.random() < 0.2:
            continue
        insert_statements.append(create_insert_statement(user['ID'], category))

        if len(insert_statements) >= 100:  # Limit the total inserts to 50
            break

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\\lietotaja_kategorija_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
