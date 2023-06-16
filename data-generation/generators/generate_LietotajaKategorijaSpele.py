import pandas as pd
import random

# Read the data
user_games = pd.read_csv('csv\\user_game_date.csv')
user_categories = pd.read_csv('csv\\user_categories.csv')

# Create a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO LietotājaKategorijaSpēle VALUES"
insert_statements.append(statement)
# Function to create an INSERT statement
def create_insert_statement(category_id, game_id):
    statement = f"\t({category_id}, {game_id}),"
    return statement

# Iterate over all categories
for _, category_row in user_categories.iterrows():
    if random.random() < 0.2:
        continue
    category_id = category_row['ID']
    user_id = category_row['UserID']
    
    # Get a list of all games owned by the user
    owned_games = user_games[user_games['UserID'] == user_id]

    # Randomly select a subset of these games
    max_categorized_games = min(3, len(owned_games))  # Limit the number of games a user can categorize to 3
    categorized_games = owned_games.sample(max_categorized_games)

    # Iterate over the categorized games
    for _, game_row in categorized_games.iterrows():
        if random.random() < 0.2:
            continue
        game_id = game_row['GameID']

        # Create the SQL INSERT statement and add it to the list
        insert_statements.append(create_insert_statement(category_id, game_id))

        # Stop after generating 150 insert statements
        if len(insert_statements) >= 150:
            break

    # Break the outer loop as well
    if len(insert_statements) >= 150:
        break

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\LietotājaKategorijaSpēle_inserts.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
