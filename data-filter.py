import pandas as pd
from googletrans import Translator

# Constants
MULT_CSV = False
filepath = "data.csv"
filepath_2 = "data_2.csv"
lang = "en"

# Read Data
df = pd.read_csv(filepath, index_col="yt-id")

# Merge multiple if needed
if MULT_CSV:
	df_2 = pd.read_csv(filepath_2, index_col="yt-id")
	df = pd.concat([df, df_2])

# Filtering data
df = df.drop_duplicates("yt-id")