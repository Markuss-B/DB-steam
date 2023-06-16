import pandas as pd
import ast
import random



# Read the data
merged_data = pd.read_csv('merged_steam_data.csv')
unique_tags = pd.read_csv('unique_tags.csv')
tag_translations = pd.read_csv('tags_with_translations.csv')

# Convert unique_tags to a list for iteration
unique_tags_list = list(unique_tags['tag'])

# Create a dictionary that maps tags to their translations
tag_translations_dict = dict(zip(tag_translations['tag'], tag_translations['translation']))

# Initialize a list to store the SQL statements
insert_statements = []

# Initialize a list to store games that have been assigned a tag
tagged_games = []


# Function to create an INSERT statement
def create_insert_statement(spele_id, genre):
    statement = f"INSERT INTO SpēleŽanrs (SpēleID, ŽanrsNosaukums) VALUES ({spele_id}, '{genre}');"
    return statement
# Ensure each tag appears at least once
for tag in unique_tags_list:
    # Find a game that contains this tag
    for index, row in merged_data.iterrows():
        tags_dict = ast.literal_eval(row['tags'])
        if tag in tags_dict.keys():
            # Prepare the values
            spele_id = index + 1  # DataFrame indices are 0-based, SQL table IDs are 1-based
            genre = tag_translations_dict.get(tag, tag).replace("'", "''")  # Use the translation if available, else use the original tag

            # Prepare the INSERT statement and add it to the list
            insert_statements.append(create_insert_statement(spele_id, genre))
            tagged_games.append(spele_id)

            # Stop looking for games with this tag
            break

# Ensure each game gets at least one tag
for index, row in merged_data.iterrows():
    spele_id = index + 1
    if spele_id not in tagged_games:
        tags_dict = ast.literal_eval(row['tags'])
        for tag in tags_dict.keys():
            if tag in unique_tags_list and create_insert_statement(spele_id, tag_translations_dict.get(tag, tag).replace("'", "''")) not in insert_statements:
                insert_statements.append(create_insert_statement(spele_id, tag_translations_dict.get(tag, tag).replace("'", "''")))
                tagged_games.append(spele_id)
                break

# Randomly select games to fill the remaining inserts
remaining_inserts = 500 - len(insert_statements)
if remaining_inserts > 0:
    untagged_indices = [i for i in range(len(merged_data)) if i+1 not in tagged_games]
    remaining_inserts = min(remaining_inserts, len(untagged_indices))
    random_indices = random.sample(untagged_indices, remaining_inserts)

    for index in random_indices:
        row = merged_data.loc[index]
        tags_dict = ast.literal_eval(row['tags'])
        for tag in tags_dict.keys():
            if tag in unique_tags_list:
                # Prepare the values
                spele_id = index + 1  # DataFrame indices are 0-based, SQL table IDs are 1-based
                genre = tag_translations_dict.get(tag, tag).replace("'", "''")  # Use the translation if available, else use the original tag

                # Prepare the INSERT statement
                statement = create_insert_statement(spele_id, genre)
                
                # Check if the statement is already in the list
                if statement not in insert_statements:
                    insert_statements.append(statement)
                    break
# Write the statements to a file
with open('genre_inserts_500.sql', 'w', encoding='utf-8') as f:
    # f.write("INSERT INTO SpēleŽanrs (SpēleID, ŽanrsNosaukums) VALUES\n")
    insert_statements[-1] = insert_statements[-1][:-1] + ';'
    for statement in insert_statements:
        f.write(statement + '\n')
