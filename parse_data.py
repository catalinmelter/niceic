import json
import pandas as pd


post_codes = pd.read_csv('D:\\Workspace\\niceic\\Postcodes.csv')['Postcode District'].values

all_data = []
for post_code in post_codes[:50]:
    print(post_code)
    data = pd.read_json("D:\\Workspace\\niceic\\dataset\\%s.txt" % post_code, lines=True)
    data = data[data['post_code'].str.contains(post_code)]
    all_data.append(data)

df = pd.concat(all_data)
df.to_csv('D:\\Workspace\\niceic\\csv\\dataset.csv')
