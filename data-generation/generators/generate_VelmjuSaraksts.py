import pandas as pd
import random
from datetime import datetime, timedelta
import numpy

# Read the data
games_data = pd.read_csv('csv\\games_date.csv')
users_data = pd.read_csv('csv\\users.csv')
users_games = pd.read_csv('csv\\user_game_date.csv')

# Convert dates from string to datetime objects
games_data['release_date'] = pd.to_datetime(games_data['release_date'])
users_data['JoinDate'] = pd.to_datetime(users_data['JoinDate'])

# Create a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO VēlmjuSaraksts VALUES"
insert_statements.append(statement)
# Define the maximum number of games per user
max_games_per_user = 10

# Define the total number of inserts
total_inserts = 300

# Iterate over all users
for _, user_row in users_data.iterrows():
    if random.random() < 0.3:
        continue

    max_games_per_user = random.randint(0, 20)

    user_id = user_row['ID']
    user_JoinDate = user_row['JoinDate']

    # Get the games that the user already owns
    owned_games_ids = users_games[users_games['UserID'] == user_id]['GameID'].tolist()

    # Exclude the games that the user already owns from the available games
    available_games = games_data[(games_data['release_date'] <= user_JoinDate) & (~games_data['ID'].isin(owned_games_ids))]

    # Randomly select a subset of these games (up to the maximum)
    owned_games = available_games.sample(min(max_games_per_user, len(available_games)))

    order = 1

    # Iterate over the owned games
    for _, game_row in owned_games.iterrows():
        if random.random() < 0.4:
            continue

        game_id = game_row['ID']
        game_release_date = game_row['release_date']

        # Generate a random acquisition date between the user's join date and now
        acquisition_date = user_JoinDate + (datetime.now() - user_JoinDate) * random.random()

        # Create the SQL INSERT statement
        statement = f"\t({user_id}, {game_id},'{acquisition_date.strftime('%Y-%m-%d')}', {order}),"
        insert_statements.append(statement)
        order += 1
        # Stop creating inserts if we have reached the desired number
        if len(insert_statements) >= total_inserts:
            break

    # Stop creating inserts if we have reached the desired number
    if len(insert_statements) >= total_inserts:
        break

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\VēlmjuSaraksts_inserts.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
