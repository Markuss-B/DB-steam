import csv

# read in the unique tags file
with open('unique_tags.csv', mode='r', encoding='utf-8-sig') as tags_file:
    tags_reader = csv.reader(tags_file)
    tags = [tag[0] for tag in tags_reader]

# read in the tag translations file
with open('unique_tags_latviski.csv', mode='r', encoding='utf-8-sig') as translations_file:
    translations_reader = csv.reader(translations_file)
    translations = [translation[0] for translation in translations_reader]

# create a new csv file that combines the tags with their translations
with open('tags_with_translations.csv', mode='w', encoding='utf-8-sig', newline='') as combined_file:
    combined_writer = csv.writer(combined_file)
    combined_writer.writerow(['Tag', 'Translation'])
    for i in range(len(tags)):
        combined_writer.writerow([tags[i], translations[i]])
