import pandas as pd
import random
from datetime import datetime

# Read the data
achievements_data = pd.read_csv('csv\\game_achievements_ids.csv')
users_data = pd.read_csv('csv\\users.csv')
user_games_data = pd.read_csv('csv\\user_game_date.csv')

# Convert dates from string to datetime objects
users_data['JoinDate'] = pd.to_datetime(users_data['JoinDate'])
user_games_data['Date'] = pd.to_datetime(user_games_data['Date'])

# Create a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO LietotājsSasniegums (LietotājsID, SasniegumsID, Datums) VALUES"
insert_statements.append(statement)

# Iterate over all users
for _, user_row in users_data.iterrows():
    user_id = user_row['ID']

    # Get a list of games that the user owns with the corresponding dates
    user_games = user_games_data[user_games_data['UserID'] == user_id]

    # Iterate over the games that the user owns
    for _, user_game_row in user_games.iterrows():
        if random.random() < 0.5:
            continue
        game_id = user_game_row['GameID']
        game_acquisition_date = user_game_row['Date']

        # Get a list of achievements for the current game
        game_achievements = achievements_data[achievements_data['GameID'] == game_id]

        # Randomly select a subset of these achievements
        owned_achievements = game_achievements.sample(min(len(game_achievements), 5))

        # Iterate over the owned achievements
        for _, achievement_row in owned_achievements.iterrows():
            if random.random() < 0.5:
                continue
            achievement_id = achievement_row['ID']

            # Generate a random achievement date between the game acquisition date and the current date
            achievement_date = game_acquisition_date + (datetime.now() - game_acquisition_date) * random.random()

            # Create the SQL INSERT statement
            statement = f"\t({user_id}, {achievement_id}, '{achievement_date.strftime('%Y-%m-%d')}'),"
            insert_statements.append(statement)

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\\LietotājsSasniegums_insert.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
