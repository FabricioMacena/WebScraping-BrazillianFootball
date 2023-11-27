# importing the libraries

import os
import pandas as pd

# removing duplicates from all datasets

for file in os.listdir(path='datas/'):
    df = pd.read_csv('datas/' + file)

    print(file)
    print(df.shape)
    df.drop_duplicates(inplace=True)
    print(df.shape)

    # saving the updated data

    df.to_csv(f'datas/{file}', index=False)
