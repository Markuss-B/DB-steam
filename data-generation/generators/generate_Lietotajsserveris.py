import pandas as pd
import random
from datetime import datetime, timedelta

def get_date():
    if random.random() < 0.6:
        date = f'DATEADD(hour, -{random.randint(1,10)}, getUTCDate())'
    else:
        date = 'NULL'
    return date

# Load the data
user_game_data = pd.read_csv('csv\\user_game_date.csv')
server_data = pd.read_csv('csv\\serveris_spele.csv')
friendship_data = pd.read_csv('csv\\friendships.csv')

# Create a list to store the SQL statements
lietotajs_spele_inserts = ["INSERT INTO LietotājsSpēlē (LietotājsID, SpēleID, ServerisID, Datums) VALUES"]

# Create a dictionary mapping from game ID to a list of its servers
game_to_servers = {}
for _, server_row in server_data.iterrows():
    game_id = server_row['GameID']
    server_id = server_row['ID']

    if game_id not in game_to_servers:
        game_to_servers[game_id] = []

    game_to_servers[game_id].append(server_id)

# Create a dictionary to store users already playing a game
users_playing = []

# For each pair of friends, if they both own the same game and that game has servers, let them play on the same server
for _, friendship_row in friendship_data.iterrows():
    user1_id = friendship_row['User1']
    user2_id = friendship_row['User2']

    # Get the games that both friends own
    user1_games = set(user_game_data[user_game_data['UserID'] == user1_id]['GameID'])
    user2_games = set(user_game_data[user_game_data['UserID'] == user2_id]['GameID'])
    common_games = user1_games & user2_games

    # For each common game, if it has servers, let them play on the same server
    for game_id in common_games:
        if game_id in game_to_servers:
            server_id = random.choice(game_to_servers[game_id])
            play_date = get_date()
            if user1_id not in users_playing:
                users_playing.append(user1_id)
                lietotajs_spele_inserts.append(f"\n\t({user1_id}, {game_id}, {server_id}, {play_date}),")
            if user2_id not in users_playing:
                users_playing.append(user2_id)
                lietotajs_spele_inserts.append(f"\n\t({user2_id}, {game_id}, {server_id}, {play_date}),")
        else:
            if random.random() < 0.2:
                continue
            server_id = 'NULL'
            play_date = get_date()
            if user1_id not in users_playing:
                users_playing.append(user1_id)
                lietotajs_spele_inserts.append(f"\n\t({user1_id}, {game_id}, {server_id}, {play_date}),")
            if user2_id not in users_playing:
                users_playing.append(user2_id)
                lietotajs_spele_inserts.append(f"\n\t({user2_id}, {game_id}, {server_id}, {play_date}),")



# Iterate over all users
for _, user_row in user_game_data.iterrows():
    if random.random() < 0.3:
        continue
    user_id = user_row['UserID']
    game_id = user_row['GameID']

    # Skip games that have no servers
    if game_id not in game_to_servers:
        server_id = 'NULL'
        if random.random() < 0.3:
            continue
    else:
        if random.random() < 0.2:
            continue
        # Randomly select a server for this game
        server_id = random.choice(game_to_servers[game_id])

    # If the user is currently playing a game, skip
    if user_id in users_playing:
        continue

    # Generate a random play date after the acquisition date
    play_date = get_date()

    users_playing.append(user_id)

    # Add to the insert statements
    lietotajs_spele_inserts.append(f"\n\t({user_id}, {game_id}, {server_id}, {play_date}),")

# Remove trailing comma from the last insert and add a semicolon
lietotajs_spele_inserts[-1] = lietotajs_spele_inserts[-1][:-1] + ';'

# Write the statements to a file
with open('inserts\\LietotājsSpēlē_inserts.sql', 'w') as f:
    for insert in lietotajs_spele_inserts:
        f.write(insert)
