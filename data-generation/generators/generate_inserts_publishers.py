import pandas as pd
import re

merged_data = pd.read_csv('merged_steam_data.csv')
founding_dates = pd.read_csv('publishers_founding_dates.csv')

unique_publishers = set()

for pub_string in merged_data['publisher']:
    pubs = pub_string.split(',')
    for pub in pubs:
        unique_publishers.add(pub.strip())

founding_dates_dict = dict(zip(founding_dates['publisher'], founding_dates['founding_date']))

# Read the existing SQL file
with open('existing_publishers_inserts.sql', 'r', encoding='utf-8') as f:
    existing_statements = f.readlines()

# Extract publisher names from the existing SQL file
existing_publishers = set()
for line in existing_statements:
    match = re.search(r"\('(.+?)',", line)
    if match:
        existing_publishers.add(match.group(1))

# Convert both sets to lowercase
lower_unique_publishers = {pub.lower() for pub in unique_publishers}
lower_existing_publishers = {pub.lower() for pub in existing_publishers}

# Remove existing publishers from the unique_publishers set
lower_unique_publishers = lower_unique_publishers.difference(lower_existing_publishers)

# Filter the original unique_publishers set based on the lowercase comparison result
unique_publishers = {pub for pub in unique_publishers if pub.lower() in lower_unique_publishers}


insert_statements = []
pubs = []
statement = f"INSERT INTO Izstrādātājs (Nosaukums, DibināšanasDatums) VALUES "
insert_statements.append(statement)

for publisher in unique_publishers:
    pub = publisher.replace("'", "''")
    founding_date = founding_dates_dict.get(publisher, 'NULL').replace(" ", "")
    # founding_date = 'NULL'
    if founding_date == 'NULL':
        statement = f"('{pub}', {founding_date}),"
    else:
        statement = f"('{pub}', '{founding_date}'),"
    insert_statements.append(statement)
    # pubs.append(pub)

insert_statements[-1] = insert_statements[-1][:-1] + ';'

with open('publishers_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')

# with open('publishers.txt', 'w', encoding='utf-8') as f:
#     for pub in pubs:
#         f.write(pub + '\n')