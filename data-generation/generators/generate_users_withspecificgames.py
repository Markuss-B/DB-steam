import pandas as pd
import random
from datetime import datetime, timedelta
import numpy

def generate_random_version():
    if random.random() < 0.6:
        return '1.0.0'
    else:
        major = random.randint(0, 3)
        minor = random.randint(0, 9)
        patch = random.randint(0, 9)
        return f'{major}.{minor}.{patch}'

games_data = pd.read_csv('csv\\games_date.csv')
users_data = pd.read_csv('csv\\users.csv')
users_game_data = pd.read_csv('csv\\user_game_date.csv')

games_data['release_date'] = pd.to_datetime(games_data['release_date'])
users_data['JoinDate'] = pd.to_datetime(users_data['JoinDate'])

insert_statements = []
statement = f"INSERT INTO LietotājsSpēle VALUES"
insert_statements.append(statement)
max_games_per_user = 3
total_inserts = 50

game_ids = [12, 15, 17, 112, 56, 60, 110]

# remove users in user_data that have games that are in game_ids
users_data = users_data[~users_data['ID'].isin(users_game_data[users_game_data['GameID'].isin(game_ids)]['UserID'])]

for _, user_row in users_data.iterrows():
    max_games_per_user = random.randint(0, 20)

    user_id = user_row['ID']
    user_JoinDate = user_row['JoinDate']

    available_games = games_data[games_data['release_date'] <= user_JoinDate]
    available_games = available_games[available_games['ID'].isin(game_ids)]

    owned_games = available_games.sample(min(max_games_per_user, len(available_games)))

    for _, game_row in owned_games.iterrows():
        game_id = game_row['ID']
        game_release_date = game_row['release_date']

        acquisition_date = user_JoinDate + (game_release_date - user_JoinDate) * random.random()

        playtime = random.randint(0, 1500)

        is_favorite = numpy.random.choice([0, 1], p=[0.8, 0.2])

        installed_version = generate_random_version()

        statement = f"\t({user_id}, {game_id}, {playtime}, '{acquisition_date.strftime('%Y-%m-%d')}', {is_favorite}, '{installed_version}'),"
        insert_statements.append(statement)
        
        if len(insert_statements) >= total_inserts:
            break

    if len(insert_statements) >= total_inserts:
        break

insert_statements[-1] = insert_statements[-1][:-1] + ';'

with open('inserts\LietotājsSpēle_papuldus_inserts.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
