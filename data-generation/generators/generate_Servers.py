import pandas as pd
import random
from faker import Faker

vardi = {1: ['Leģendārās', 'Lāčplēša', 'Melnās', 'Jūras', 'Zelta', 'Pilsētas', 'Kosmosa', 'Reģiona', 'Ziemeļu', 'Vēju', 'Vētras', 'Karalienes', 'Lielās', 'Senču', 'Pēdējās', 'Cerības', 'Dvēseļu', 'Kalna', 'Draudzīgā', 'Burvju'],
         2: ['Cīņas', 'Pirātu', 'Izdzīvošana', 'Izpētītāji', 'Pasaule', 'Valstība', 'Meža', 'Bastions', 'Mistērija', 'Akadēmija']}

# Initialize faker
fake = Faker()

# Read the multiplayer games data
multiplayer_games_data = pd.read_csv('csv\\multiplayer.csv')

# Define a list to store the SQL statements
server_inserts = ["INSERT INTO Serveris (IPAddress, Port, Nosaukums, SpēleID) VALUES"]

# Create a set to store used IP:Port combinations
used_ip_ports = set()

# Iterate over all multiplayer games
for _, game_row in multiplayer_games_data.iterrows():
    if random.random() < 0.2:
        continue
    game_id = game_row['ID']

    # Determine the number of servers for this game (between 0 and 10)
    num_servers = random.randint(0, 10)

    for _ in range(num_servers):
        while True:
            # Generate a random IP address
            ip_address = fake.ipv4()

            # Generate a random port number
            port = random.randint(1000, 9999)

            # If the IP:Port combination is unique, break the loop
            if (ip_address, port) not in used_ip_ports:
                used_ip_ports.add((ip_address, port))
                break

        # Generate a random server name
        word1 = random.choice(vardi[1])
        # word2 is a random word from vardi[1] that isn't the same as word1
        word2 = random.choice([word for word in vardi[1] if word != word1])
        word3 = random.choice(vardi[2])

        name = f"{word1} {word2} {word3}"

        # Add to the server inserts
        server_inserts.append(f"\n\t('{ip_address}', {port}, '{name}', {game_id}),")

# Remove trailing comma from the last insert and add a semicolon
server_inserts[-1] = server_inserts[-1][:-1] + ';'

# Write the statements to a file
with open('inserts\\Serveris_inserts.sql', 'w') as f:
    for insert in server_inserts:
        f.write(insert)
