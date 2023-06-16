import pandas as pd
import random
from faker import Faker

list_1 = ["Draudzīgā", "Leģendārā", "Melnās", "Zelta", "Kosmosa", "Ziemeļu", "Vētras", "Lielās", "Pēdējās", "Dvēseļu", "Burvju"]
list_2 = ["Jūras", "Pilsētas", "Reģiona", "Vēju", "Karalienes", "Senču", "Cerības", "Kalna", "Akadēmijas", "Lāčplēša", "Bastions"]
list_3 = ["Pirātu", "Izdzīvošanas", "Izpētītāju", "Pasaules", "Valstības", "Meža", "Tūre", "Mistērijas", "Paradīzes", "Cīņas"]
list_4 = ["Cepure", "Jaka", "Iešana", "ŅSG", "M4A4", "Zobens", "Krekls", "Bikses", "Dzelzs", "Ķivere", "Zirgs", "Maģija", "Pilis", "Kaujas Āmurs", "Plēve", "Ķēde", "Šaržieris", "Bulta", "Ķirsis", "Bumba"]

descs = {"Cepure": "Šī cepure ir izgatavota no visizturīgākajiem materiāliem, lai aizsargātu jūs pret sauli un lietu.",
"Jaka": "Šī jaka ir silta un ērta, ideāli piemērota ilgām ceļojuma dienām.",
"Iešana": "Iešana ir līdzinieks jebkura karavīra arsenālā, gatavs pārsteigt ienaidniekus.",
"ŅSG": "Ar precīzu mērķēšanu un lielu kaitējumu, ŅSG ir perfekta izvēle cīņai.",
"M4A4": "M4A4 piedāvā stabilu uguni un precīzu mērķēšanu, lai apkarotu jebkuru draudu.",
"Zobens": "Zobens ir klasiskas cīņas simbols, spēcīgs un bīstams ierocis.",
"Krekls": "Šis krekls ir izgatavots no ērtiem un izturīgiem materiāliem, lai jūs varētu ceļot ar stilu.",
"Bikses": "Izgatavots no augstas kvalitātes sastāvdaļām, šis Bikses nodrošina lielisku atveseļošanos.",
"Dzelzs": "Dzelzs ir būtiska materiāla sastāvdaļa daudzu ieroču un bruņu ražošanā.",
"Ķivere": "Ķivere ir būtiska aizsardzība kaujā, kas aizsargā pret smagiem triecieniem."}

# Initialize Faker with Latvian locale
fake = Faker('lv_LV')

# Read the data
game_data = pd.read_csv('csv\\games_date.csv')
multiplayer_game_data = pd.read_csv('csv\\multiplayer.csv')

# Create a set of multiplayer game IDs for easy lookup
multiplayer_game_ids = set(multiplayer_game_data['ID'])

# Create a list to store the SQL statements
mantas_klase_inserts = ["INSERT INTO MantasKlase (Nosaukums, Apraksts, SpēleID) VALUES"]

# Iterate over all games
for _, game_row in game_data.iterrows():
    game_id = game_row['ID']

    if game_id not in multiplayer_game_ids:
        if random.random() < 0.5:
            continue
    
    # Generate a random number of classes for this game
    # Multiplayer games have a higher chance of having more classes
    num_classes = random.randint(3, 10) if game_id in multiplayer_game_ids else random.randint(1, 5)

    for _ in range(num_classes):
        # Generate a random class name and description
        class_name = ""
        name1 = ""
        name2 = ""
        name3 = ""
        name4 = random.choice(list_4)
        if random.random() < 0.5:
            name1 = random.choice(list_1)
            class_name += name1 + " "
        if random.random() < 0.5:
            name2 = random.choice(list_2)
            class_name += name2 + " "
        if random.random() < 0.5:
            name3 = random.choice(list_3)
            class_name += name3 + " "
        class_name += name4
        
        if class_name in descs:
            class_description = "'" + descs[class_name] + "'"
        elif random.random() < 0.5:
            class_description = "'" + fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None) + "'"
        else:
            class_description = 'NULL'

        # Add to the insert statements
        mantas_klase_inserts.append(f"\n\t('{class_name}', {class_description}, {game_id}),")

# Remove trailing comma from the last insert and add a semicolon
mantas_klase_inserts[-1] = mantas_klase_inserts[-1][:-1] + ';'

# Write the statements to a file
with open('inserts\\MantasKlase_inserts.sql', 'w') as f:
    for insert in mantas_klase_inserts:
        f.write(insert)
