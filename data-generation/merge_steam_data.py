import pandas as pd

steam_app_data = pd.read_csv('data\download\steam_app_data.csv')
steamspy_data = pd.read_csv('data\download\steamspy_data.csv')

merged_data = pd.merge(steam_app_data, steamspy_data, left_on='steam_appid', right_on='appid')

merged_data = merged_data.drop(columns=['appid', 'name_y'])
merged_data = merged_data.rename(columns={'name_x': 'name'})

merged_data.to_csv('merged_steam_data.csv', index=False)
