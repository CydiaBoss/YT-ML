import pandas as pd

# Merge both datasets
filepath_1 = "data_1.csv"
filepath_2 = "data_1.csv"
df_1 = pd.read_csv(filepath_1, index_col="yt-id")
df_2 = pd.read_csv(filepath_2, index_col="yt-id")

combined_data = pd.concat([df_1, df_2])

# Filtering data
combined_data.drop_duplicates(["yt-id",])