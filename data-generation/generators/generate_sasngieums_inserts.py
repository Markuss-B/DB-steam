import pandas as pd

# Read the data
achievements_data = pd.read_csv('game_achievements.csv')

# Create a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO Sasniegums (Nosaukums, Teksts, SpēleID) VALUES"
insert_statements.append(statement)

# Iterate over all rows in the data
for _, row in achievements_data.iterrows():
    game_id = row['GameID']
    name = row['Name'].replace('"', '').replace("'", "''")
    text = row['Text'].replace("'", "''")

    # Create the SQL INSERT statement
    statement = f"\t('{name}', '{text}', {game_id}),"
    insert_statements.append(statement)

# Remove the last comma and add a semicolon
insert_statements[-1] = insert_statements[-1][:-1] + ';'

# Write the statements to a file
with open('sasniegums_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
