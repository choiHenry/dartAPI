import dapi

my_api = dapi.Dapi()
# my_api.get_affiliate_num(2019)

my_api.concat_files('./data/kiscode2019')

# import pandas as pd
# df = pd.read_excel('./data/kiscode2019/kiscode_DB_2019.xlsx', engine='openpyxl')
# print(df.head())