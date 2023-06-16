import pandas as pd
import random
from datetime import datetime, timedelta
import math

predefined_reviews = {
    1: [
        "Spēle ir pilnīga vilšanās. Nav vērts ne mirkli.",
        "Absolūti neaizraujoša. Tas bija manas naudas tērējums.",
        "Nebūtu vajadzējis pirkt. Pilns ar tehniskām problēmām.",
        "Nedomāju, ka kāds varētu izbaudīt šo spēli. Pilnīgi šausmīga.",
        "Viens no sliktākajiem pirkumiem, ko esmu veicis. Negribu vairs spēlēt."
    ],
    2: [
        "Spēle ir zem vidējā. Daudz kļūdu un problēmu.",
        "Spēle ir neaizraujoša un tā mani ātri apnika.",
        "Spēle ir grūti saprotama un bieži vien frustrējoša.",
        "Man nepatīk šī spēle. Tas bija vairāk kā mācību process nekā izklaide.",
        "Spēles dizains un vides ir slikta kvalitāte. Nav patīkami."
    ],
    3: [
        "Spēle ir vidēja. Tas nav slikts, bet arī nav labs.",
        "Šī spēle ir tikai ok. Es varētu to ieteikt, ja tas ir izpārdošanā.",
        "Spēle ir labi strukturēta, bet ir pārāk daudz atkārtošanās.",
        "Spēle varētu būt daudz labāka ar dažiem uzlabojumiem.",
        "Spēle ir vidēja, bet ir daži interesanti momenti."
    ],
    4: [
        "Šī spēle ir diezgan laba, tomēr ir daži trūkumi.",
        "Man patīk šī spēle, bet tā varētu būt labāka.",
        "Spēle ir aizraujoša un grafika ir laba, bet stāsts ir mazliet vājš.",
        "Šī spēle ir laba, bet tai ir nepieciešams vairāk atjauninājumu.",
        "Spēle ir interesanta, bet ir daži tehniski jautājumi, kas jāatrisina."
    ],
    5: [
        "Šī spēle ir fantastiska! Es to spēlēju katru dienu.",
        "Viens no labākajiem pirkumiem, ko esmu veicis. Pārsteidzoša spēle.",
        "Brīnišķīga spēle ar lielisku stāstu un grafiku.",
        "Šī ir viena no manām mīļākajām spēlēm. Noteikti ieteiktu.",
        "Šī spēle ir absolūti brīnišķīga. Es nevaru pārtraukt to spēlēt."
    ]
}


# Read the data
users_data = pd.read_csv('csv\\users.csv')
user_game_data = pd.read_csv('csv\\user_game_date.csv')

# Create a list to store the SQL statements
review_inserts = ["INSERT INTO Recenzija (LietotājsID, SpēleID, Teksts, Vērtējums, Datums) VALUES"]

# Iterate over all users
for _, user_row in users_data.iterrows():
    if random.random() < 0.3:
        continue
    user_id = user_row['ID']

    # Get the games that the user owns
    user_games = user_game_data[user_game_data['UserID'] == user_id]

    # Iterate over each game the user owns
    for _, game_row in user_games.iterrows():
        if random.random() < 0.5:
            continue
        game_id = game_row['GameID']
        game_acquisition_date = game_row['Date']

        # Generate a random review date after the acquisition date
        review_date = datetime.strptime(game_acquisition_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 100))

        # Generate a random review score
        review_score = random.randint(1, 10)

        # Generate a random review text
        if random.random() < 0.5:
            review_text = "'" + random.choice(predefined_reviews[math.ceil(review_score/2)]) + "'"
        else:
            review_text = 'NULL'

        # Add to the review inserts
        review_inserts.append(f"\n\t({user_id}, {game_id}, {review_text}, {review_score}, '{review_date.strftime('%Y-%m-%d')}'),")


# Remove trailing comma from the last insert and add a semicolon
review_inserts[-1] = review_inserts[-1][:-1] + ';'

# Write the statements to a file
with open('inserts\\Recenzija_inserts.sql', 'w') as f:
    for insert in review_inserts:
        f.write(insert)
