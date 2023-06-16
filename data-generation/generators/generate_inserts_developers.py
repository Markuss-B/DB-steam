import pandas as pd
import re

merged_data = pd.read_csv('merged_steam_data.csv')
founding_dates = pd.read_csv('founding_dates.csv')

unique_developers = set()

for dev_string in merged_data['developer']:
    devs = dev_string.split(',')
    for dev in devs:
        unique_developers.add(dev.strip())

founding_dates_dict = dict(zip(founding_dates['developer'], founding_dates['founding_date']))

# Read the existing SQL file
with open('existing_developers_inserts.sql', 'r', encoding='utf-8') as f:
    existing_statements = f.readlines()

# Extract developer names from the existing SQL file
existing_developers = set()
for line in existing_statements:
    match = re.search(r"\('(.+?)',", line)
    if match:
        existing_developers.add(match.group(1))

# Convert both sets to lowercase
lower_unique_developers = {dev.lower() for dev in unique_developers}
lower_existing_developers = {dev.lower() for dev in existing_developers}

# Remove existing developers from the unique_developers set
lower_unique_developers = lower_unique_developers.difference(lower_existing_developers)

# Filter the original unique_developers set based on the lowercase comparison result
unique_developers = {dev for dev in unique_developers if dev.lower() in lower_unique_developers}


insert_statements = []
statement = f"INSERT INTO Izstrādātājs (Nosaukums, DibināšanasDatums) VALUES "
insert_statements.append(statement)

for developer in unique_developers:
    dev = developer.replace("'", "''")
    founding_date = founding_dates_dict.get(developer, 'NULL').replace(" ", "")
    if founding_date == 'NULL':
        statement = f"('{dev}', {founding_date}),"
    else:
        statement = f"('{dev}', '{founding_date}'),"
    insert_statements.append(statement)

insert_statements[-1] = insert_statements[-1][:-1] + ';'

with open('developers_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
