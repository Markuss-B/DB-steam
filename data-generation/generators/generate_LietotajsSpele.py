import pandas as pd
import random
from datetime import datetime, timedelta
import numpy
def generate_random_version():
    # Most of the time, return '1.0.0'
    if random.random() < 0.6:  # 90% of the time
        return '1.0.0'
    else:  # 10% of the time, generate a random version
        major = random.randint(0, 3)
        minor = random.randint(0, 9)
        patch = random.randint(0, 9)
        return f'{major}.{minor}.{patch}'

# Read the data
games_data = pd.read_csv('csv\\games_date.csv')
users_data = pd.read_csv('csv\\users.csv')

# Convert dates from string to datetime objects
games_data['release_date'] = pd.to_datetime(games_data['release_date'])
users_data['JoinDate'] = pd.to_datetime(users_data['JoinDate'])

# Create a list to store the SQL statements
insert_statements = []
statement = f"INSERT INTO LietotājsSpēle VALUES"
insert_statements.append(statement)
# Define the maximum number of games per user
max_games_per_user = 10

# Define the total number of inserts
total_inserts = 1000

specific_game_ids = [12, 15, 17, 112, 56, 60, 110]
# get those games data
specific_games_data = games_data[games_data['ID'].isin(specific_game_ids)]

# exclude specifig games data from games dta
games_data = games_data[~games_data['ID'].isin(specific_game_ids)]

# Iterate over all users
for _, user_row in users_data.iterrows():
    if random.random() < 0.2:
        continue
    max_games_per_user = random.randint(0, 20)

    user_id = user_row['ID']
    user_JoinDate = user_row['JoinDate']

    # Select a random subset of games 
    owned_games = games_data.sample(max_games_per_user)

    # Concat specific games to the list of owned games
    owned_games = pd.concat([owned_games, specific_games_data])

    dates = []
    # Iterate over the owned games
    for _, game_row in owned_games.iterrows():
        if random.random() < 0.2:
            continue
        game_id = game_row['ID']
        game_release_date = game_row['release_date']
        # Generate a random acquisition date between the user's join date and the game's release date
        if pd.isnull(game_release_date):
            game_release_date = user_JoinDate
        acquisition_date = user_JoinDate + (game_release_date - user_JoinDate) * random.random()
        # if dates isn't empty choose a random date to be the acquisition date aslong as the acquisition date is after game release date
        if [date for date in dates if date > game_release_date]:
            if random.random() < 0.5:
                randChoice = random.choice([date for date in dates if date > game_release_date])
                if randChoice:
                    acquisition_date = randChoice
                else:
                    dates.append(acquisition_date)
            else:
                dates.append(acquisition_date)
        else:
            dates.append(acquisition_date)
        # Generate a random playtime (in hours)
        playtime = random.randint(0, 1500)

        # Randomly decide whether the game is favorited
        is_favorite = numpy.random.choice([0, 1], p=[0.8, 0.2])

        # Generate a random version number
        installed_version = generate_random_version()

        # Create the SQL INSERT statement
        statement = f"\t({user_id}, {game_id}, {playtime}, '{acquisition_date.strftime('%Y-%m-%d')}', {is_favorite}, '{installed_version}'),"
        insert_statements.append(statement)
        
        # Stop creating inserts if we have reached the desired number
        if len(insert_statements) >= total_inserts:
            break

    # Stop creating inserts if we have reached the desired number
    if len(insert_statements) >= total_inserts:
        break

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\LietotājsSpēle_inserts.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
