import pandas as pd
import re

merged_data = pd.read_csv('merged_steam_data.csv')

unique_tags = set()

# Regular expression to match tag names
tag_pattern = re.compile(r"'([^']+)':")

for tags_string in merged_data['tags']:
    tags = tag_pattern.findall(tags_string)
    unique_tags.update(tags)

# Save unique tags to a CSV file
tags_df = pd.DataFrame(list(unique_tags), columns=['tag'])
tags_df.to_csv('unique_tags.csv', index=False)
