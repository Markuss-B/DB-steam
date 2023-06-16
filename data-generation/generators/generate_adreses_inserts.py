from faker import Faker
import random

countries = {
    'Latvija': [
        {'City': 'Rīga', 'Postcode': 'LV-1000'},
        {'City': 'Liepāja', 'Postcode': 'LV-3401'},
        {'City': 'Daugavpils', 'Postcode': 'LV-5401'}
    ],
    'Igaunija': [
        {'City': 'Tallina', 'Postcode': 'EE-10111'},
        {'City': 'Tartu', 'Postcode': 'EE-51001'},
        {'City': 'Pärnu', 'Postcode': 'EE-80010'}
    ],
    'Lietuva': [
        {'City': 'Vilnius', 'Postcode': 'LT-01100'},
        {'City': 'Kaunas', 'Postcode': 'LT-44240'},
        {'City': 'Klaipėda', 'Postcode': 'LT-91234'}
    ],
    'Somija': [
        {'City': 'Helsinki', 'Postcode': 'FI-00100'},
        {'City': 'Tampere', 'Postcode': 'FI-33100'},
        {'City': 'Turku', 'Postcode': 'FI-20100'}
    ],
    'Zviedrija': [
        {'City': 'Stokholma', 'Postcode': 'SE-11120'},
        {'City': 'Gotenburga', 'Postcode': 'SE-41101'},
        {'City': 'Malmē', 'Postcode': 'SE-21110'}
    ],
    'Norvēģija': [
        {'City': 'Osla', 'Postcode': 'NO-0010'},
        {'City': 'Bergena', 'Postcode': 'NO-5001'},
        {'City': 'Stavangera', 'Postcode': 'NO-4016'}
    ],
    'Dānija': [
        {'City': 'Kopenhāgena', 'Postcode': 'DK-1050'},
        {'City': 'Aarhusa', 'Postcode': 'DK-8000'},
        {'City': 'Aalborga', 'Postcode': 'DK-9000'}
    ],
    'Vācija': [
        {'City': 'Berlīne', 'Postcode': 'DE-10117'},
        {'City': 'Münchena', 'Postcode': 'DE-80331'},
        {'City': 'Hamburga', 'Postcode': 'DE-20095'}
    ],
    'Kanāda': [
        {'City': 'Toronto', 'Postcode': 'M5G'},
        {'City': 'Montreāla', 'Postcode': 'H2X'},
        {'City': 'Vankūvera', 'Postcode': 'V6C'}
    ],
    'Nīderlande': [
        {'City': 'Amsterdama', 'Postcode': 'NL-1012'},
        {'City': 'Roterdama', 'Postcode': 'NL-3011'},
        {'City': 'Hāga', 'Postcode': 'NL-2511'}
    ]
}


# Use the Latvian localization
fake = Faker('lv_LV')

# Create a list to store the SQL statements
insert_statements = []
statement = "INSERT INTO NorēķinuAdrese (Valsts, Pilsēta, Iela, MājasNr, DzīvokļaNr, PastaIndekss) VALUES"
insert_statements.append(statement)

# Function to create an INSERT statement
def create_insert_statement(valsts, pilseta, iela, majasnr, dzivoklinr, pastaindekss):
    statement = f"\t('{valsts}', '{pilseta}', '{iela}', '{majasnr}', '{dzivoklinr}', '{pastaindekss}'),"
    return statement

# Generate 30 addresses
for country in countries:
    for city in countries[country]:
        valsts = country
        pilseta = city['City']
        iela = fake.street_name()
        majasnr = fake.building_number()
        dzivoklinr = random.randint(1, 100)  # Random apartment number between 1 and 100
        pastaindekss = city['Postcode']
        insert_statements.append(create_insert_statement(valsts, pilseta, iela, majasnr, dzivoklinr, pastaindekss))

insert_statements[-1] = insert_statements[-1][:-1] + ';'
# Write the statements to a file
with open('inserts\\norekinu_adrese_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
