import pandas as pd
import random
from datetime import datetime, timedelta

# Read the users data
users_data = pd.read_csv('csv\\users.csv')
existing_friendships = pd.read_csv('csv\\friendships.csv')

# Convert JoinDate to datetime
users_data['JoinDate'] = pd.to_datetime(users_data['JoinDate'])

# Filter out users who joined after 2022
users_data = users_data[users_data['JoinDate'] < datetime(2023, 1, 1)]

# Initialize a list to store the SQL statements
insert_statements = []

# Function to create an INSERT statement
def create_insert_statement(user1, user2, date):
    date = date.strftime('%Y-%m-%d')
    return f"({user1}, {user2}, '{date}')"

# Initialize a set to store the already created friendships
created_friendships = set()
created_friendships.update(zip(existing_friendships['User1'], existing_friendships['User2']))

# Generate the friendships
for i in range(100):
    # Select two random users
    user1, user2 = random.sample(range(len(users_data)), 2)
    user1_id = users_data.iloc[user1]['ID']
    user2_id = users_data.iloc[user2]['ID']
    if (user1_id, user2_id) not in created_friendships and (user2_id, user1_id) not in created_friendships:
        # Check the join dates
        user1_join_date = users_data.iloc[user1]['JoinDate']
        user2_join_date = users_data.iloc[user2]['JoinDate']

        # The date of the friendship should be after both users have joined
        friendship_date = max(user1_join_date, user2_join_date) + timedelta(days=random.randint(1, 365))

        # Prepare the INSERT statement and add it to the list
        insert_statements.append(create_insert_statement(user1_id, user2_id, friendship_date))
        insert_statements.append(create_insert_statement(user2_id, user1_id, friendship_date))

        # Remember this friendship to avoid duplicates
        created_friendships.add((user1_id, user2_id))
        created_friendships.add((user2_id, user1_id))

# Generate the final script
final_script = "INSERT INTO Friendships (User1, User2, Date) VALUES\n" + ",\n".join(insert_statements) + ";"

# Write the final script to a file
with open('inserts\\friendships_inserts22.sql', 'w', encoding='utf-8') as f:
    f.write(final_script)
