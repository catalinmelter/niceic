import pandas as pd


print(pd.read_csv('csv\\dataset.csv')[['start_of_post_code', 'post_code']])