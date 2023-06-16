import pandas as pd
import ast

# Read the data
merged_data = pd.read_csv('merged_steam_data.csv')
unique_tags = pd.read_csv('unique_tags.csv')
tag_translations = pd.read_csv('tags_with_translations.csv')

# Convert unique_tags to a set for faster lookup
unique_tags_set = set(unique_tags['tag'])

# Create a dictionary that maps tags to their translations
tag_translations_dict = dict(zip(tag_translations['tag'], tag_translations['translation']))

# Initialize a list to store the SQL statements
insert_statements = []

statement = f"INSERT INTO SpēleŽanrs (SpēleID, ŽanrsNosaukums) VALUES "
insert_statements.append(statement)
# Iterate through the DataFrame rows
for index, row in merged_data.iterrows():
    # Parse the tags string into a dictionary
    tags_dict = ast.literal_eval(row['tags'])

    # Iterate through the tags
    for tag in tags_dict.keys():
        # If the tag is in unique_tags_set, prepare an INSERT statement
        if tag in unique_tags_set:
            # Prepare the values
            spele_id = index + 1  # DataFrame indices are 0-based, SQL table IDs are 1-based
            genre = tag_translations_dict.get(tag, tag).replace("'", "''")  # Use the translation if available, else use the original tag

            # Prepare the INSERT statement
            statement = f"\t({spele_id}, '{genre}'),"

            # Add the statement to the list
            insert_statements.append(statement)

insert_statements[-1] = insert_statements[-1][:-1] + ';'

# Write the statements to a file
with open('spelezanrs_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')
