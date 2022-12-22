import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
from collections import OrderedDict
import sys

parser = argparse.ArgumentParser(description="language parser")

parser.add_argument("language", action="store")

# get args
args = parser.parse_args()
language = args.language

url = f"https://1000mostcommonwords.com/1000-most-common-{language}-words/"
try:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')
    df_dict = OrderedDict()
    for i in range(len(rows)):
        row = rows[i]
        items = row.findAll(lambda tag: tag.name == 'td')

        if i == 0:
            for item in items:
                df_dict[item.text.lower()] = []
            df_dict_keys = list(df_dict.keys())
            continue

        for i in range(len(items)):
            key = df_dict_keys[i]
            item = items[i].text
            df_dict[key].append(items[i].text)

    df = pd.DataFrame(df_dict, columns=df_dict.keys())

except Exception:
    print("Please enter a valid language from 1000mostcommonwords.com. Ensure the spelling is correct")
    sys.exit(1)


print(df.head())
file_path = f'top_{language}_1000_words'
df.to_csv(file_path)
