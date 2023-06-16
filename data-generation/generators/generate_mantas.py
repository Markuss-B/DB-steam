import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker with Latvian locale
fake = Faker('lv_LV')

vards1 = ["Dieva", "Māģiskā", "Lokā", "Slazdo", "Gudrības", "Spēka", "Nekro", "Bezmiegs", "Šāviens", "Skaļais", "Birstošā", "Zelta", "Nāves", "Neredzamais", "Sarkanā", "Spēka", "Ierocis", "Varoņa"]

vards2 = ["Briesmonis", "Mistika", "ugunskrusts", "Dūmi", "Akmens", "Pulveris", "Noslēpums", "Bērzs", "Sirds", "Smeķis", "Zirneklītis", "Salūts", "Pūlis", "Asass", "Lāse", "Sprādziens", "Vārdu", "Aptieka"]


# Load the data
user_game_data = pd.read_csv('csv\\user_game_date.csv')
item_class_data = pd.read_csv('csv\\itemclass_gameid.csv')

# Create a dictionary mapping from game ID to a list of its item classes
game_to_item_classes = {}
for _, row in item_class_data.iterrows():
    game_id = row['gameid']
    class_id = row['classid']

    if game_id not in game_to_item_classes:
        game_to_item_classes[game_id] = []

    game_to_item_classes[game_id].append(class_id)

# Create a list to store the SQL statements
manta_inserts = ["INSERT INTO Manta (ĪpašnieksID, MantasKlaseID, DotaisVārds, IzveidesDatums) VALUES"]
mantas_ipasnieku_vesture_inserts = ["INSERT INTO MantasĪpašniekuVēsture (LietotājsID, MantaID, DatumsLīdz) VALUES"]

# Keep track of item IDs
item_id = 1
last_user = 0
# Iterate over all users
for _, user_row in user_game_data.iterrows():
    if last_user == user_row['UserID']:
        if random.random() < 0.5:
            continue
    if random.random() < 0.5:
        last_user = user_row['UserID']
        continue

    user_id = user_row['UserID']
    game_id = user_row['GameID']
    last_user = user_id
    game_acquisition_date = datetime.strptime(user_row['Date'], '%Y-%m-%d')

    # Skip games that have no item classes
    if game_id not in game_to_item_classes:
        continue

    # Generate a random number of items for this user and game
    num_items = random.randint(0, 5)

    for _ in range(num_items):
        # Randomly select an item class for this item
        class_id = random.choice(game_to_item_classes[game_id])

        # Generate a random item name
        if random.random() < 0.5:
            item_name = "'" + vards1[random.randint(0, len(vards1)-1)] + " " + vards2[random.randint(0, len(vards2)-1)] + "'"
        else:
            item_name = 'NULL'

        # Generate a random creation date after the acquisition date and before the end of 2023
        creation_date = game_acquisition_date + timedelta(days=random.randint(0, (datetime(2023, 5, 25) - game_acquisition_date).days)) + + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

        # Add to the insert statements
        manta_inserts.append(f"\n\t({user_id}, {class_id}, {item_name}, '{creation_date.strftime('%Y-%m-%d %H:%M:%S')}'),")
        
        # Generate a random number of previous owners
        num_previous_owners = random.randint(0, 5)
        owner_history = []
        for _ in range(num_previous_owners):
            # Randomly select a previous owner who is not the current owner and owned the game before the item's creation date
            previous_owner_candidates = [u for _, u in user_game_data[(user_game_data['UserID'] != user_id) & (user_game_data['GameID'] == game_id) & (user_game_data['Date'] < creation_date.strftime('%Y-%m-%d'))].iterrows()]
            newlist = []
            for owner in previous_owner_candidates:
                if owner['UserID'] not in owner_history:
                    newlist.append(owner)
            previous_owner_candidates = newlist
            if not previous_owner_candidates:
                continue
            previous_owner = random.choice(previous_owner_candidates)

            previous_owner['Date'] = datetime.strptime(previous_owner['Date'], '%Y-%m-%d')
            # Generate a random end date for the previous owner before the current owner's creation date and before 2023
            max_end_date = min(creation_date + timedelta(days=random.randint(0, (creation_date - previous_owner['Date']).days)), datetime(2023, 5, 25))
            end_date = min(max_end_date, datetime(2023, 5, 25))
            end_date += timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            # Add an entry to the item ownership history
            owner_history.append((previous_owner['UserID']))
            mantas_ipasnieku_vesture_inserts.append(f"\n\t({previous_owner[0]}, {item_id}, '{end_date.strftime('%Y-%m-%d %H:%M:%S')}'),")
            if end_date == datetime(2023, 5, 25):
                break
            if random.random() < 0.5:
                break

        # Increment item ID
        item_id += 1

# Remove trailing comma from the last inserts and add a semicolon
manta_inserts[-1] = manta_inserts[-1][:-1] + ';'
mantas_ipasnieku_vesture_inserts[-1] = mantas_ipasnieku_vesture_inserts[-1][:-1] + ';'

# Write the statements to files
with open('inserts\\Manta_inserts.sql', 'w') as f:
    for insert in manta_inserts:
        f.write(insert)

with open('inserts\\MantasĪpašniekuVēsture_inserts.sql', 'w') as f:
    for insert in mantas_ipasnieku_vesture_inserts:
        f.write(insert)
