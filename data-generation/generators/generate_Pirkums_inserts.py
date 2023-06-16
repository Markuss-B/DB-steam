import pandas as pd
import random
from datetime import datetime, timedelta
import numpy

# Read the data
users_data = pd.read_csv('csv\\users.csv')
user_game_data = pd.read_csv('csv\\user_game_date.csv')
game_prices = pd.read_csv('csv\\game_price.csv')
user_addresses = pd.read_csv('csv\\user_NorekinuAdreseID.csv')

# Define payment methods
payment_methods = ['Visa', 'MasterCard', 'PayPal']

# Define a counter for the purchase ID
purchase_id = 1

# Create a list to store the SQL statements
purchase_inserts = ["INSERT INTO Pirkums (LietotājsID, Datums, Summa) VALUES"]
game_inserts = ["INSERT INTO PirkumaSpēle (PirkumsID, SpēleID, Cena) VALUES"]
payment_inserts = ["INSERT INTO Maksājums (MaksājumaMetode, KartesCipari, NorēķinuAdreseID, PirkumsID) VALUES"]

# Iterate over all users
for _, user_row in users_data.iterrows():
    user_id = user_row['ID']
    user_address_id = user_addresses[user_addresses['ID'] == user_id]['NorekinuAdreseID'].values[0]

    # Get the games that the user owns
    user_games = user_game_data[user_game_data['UserID'] == user_id]

    # Group games by acquisition date
    user_games_by_date = user_games.groupby('Date')

    # Iterate over each acquisition date
    for acquisition_date, games_on_date in user_games_by_date:
        total_price = 0
        # if only 1 game for date then random chane of not buying
        if len(games_on_date) == 1:
            if random.random() < 0.2:
                continue
        # Iterate over each game acquired on this date
        for _, game_row in games_on_date.iterrows():
            game_id = game_row['GameID']

            # Get the price of the game
            game_price = game_prices[game_prices['ID'] == game_id]['price'].values[0]
            if game_price == 0:
                continue
            elif random.random() < 0.1:
                continue


            # Occasionally apply a discount
            if random.random() < 0.1:  # 10% chance of a discount
                game_price *= (random.choice([5, 10, 15, 25, 30, 45, 50, 75, 90])/100)  # Discount between 10% and 50%
            
            game_price = round(game_price, 2)

            total_price += game_price

            # Add to the game inserts
            game_inserts.append(f"\n\t({purchase_id}, {game_id}, {game_price}),")
        if total_price == 0:
            continue
        # Add to the purchase inserts
        purchase_inserts.append(f"\n\t({user_id}, '{acquisition_date}', {round(total_price, 2)}),")

        # Generate a random payment method
        payment_method = random.choice(payment_methods)

        # Generate a random card number
        if payment_method == 'PayPal':
            card_number = 'NULL'
        else:
            card_number = "'" + str(random.randint(1000, 9999)) + "'"

        # Add to the payment inserts
        payment_inserts.append(f"\n\t('{payment_method}', {card_number}, {user_address_id}, {purchase_id}),")

        purchase_id += 1

# Remove trailing comma from the last insert and add a semicolon
purchase_inserts[-1] = purchase_inserts[-1][:-1] + ';'
game_inserts[-1] = game_inserts[-1][:-1] + ';'
payment_inserts[-1] = payment_inserts[-1][:-1] + ';'

# Write the statements to files
with open('inserts\\Pirkums_PirkumaSPele_Maksajums_inserts.sql', 'w') as f:
    for insert in purchase_inserts:
        f.write(insert)
    f.write('\n\n')
    for insert in game_inserts:
        f.write(insert)
    f.write('\n\n')
    for insert in payment_inserts:
        f.write(insert)
# with open('inserts\\Pirkums_inserts.sql', 'w') as f:
#     for insert in purchase_inserts:
#         f.write(insert)

# with open('inserts\\PirkumaSpele_inserts.sql', 'w') as f:
#     for insert in game_inserts:
#         f.write(insert)

# with open('inserts\\Maksājums_inserts.sql', 'w') as f:
#     for insert in payment_inserts:
#         f.write(insert)
