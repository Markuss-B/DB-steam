import pandas as pd
import re

tags_file = pd.read_csv('unique_tags_latviski.csv')


# Read the existing SQL file
with open('existing_tags_inserts.sql', 'r', encoding='utf-8') as f:
    existing_statements = f.readlines()

# Extract tag names from the existing SQL file
existing_tags = set()
for line in existing_statements:
    match = re.search(r"\('(.+?)',", line)
    if match:
        existing_tags.add(match.group(1))

# Convert both sets to lowercase
lower_unique_tags = {tag.lower() for tag in tags_file['tag']}
lower_existing_tags = {tag.lower() for tag in existing_tags}

# Remove existing tags from the unique_tags set
lower_unique_tags = lower_unique_tags.difference(lower_existing_tags)

# Filter the original unique_tags set based on the lowercase comparison result
tags_file = tags_file[tags_file['tag'].str.lower().isin(lower_unique_tags)]

unique_tags = set()

for dev_string in tags_file['tag']:
    devs = dev_string.split(',')
    for dev in devs:
        unique_tags.add(dev.strip())

insert_statements = []
statement = f"INSERT INTO Žanrs (Nosaukums) VALUES "
insert_statements.append(statement)

for tag in unique_tags:
    statement = f"('{tag}'),"
    insert_statements.append(statement)

insert_statements[-1] = insert_statements[-1][:-1] + ';'

with open('tags_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
