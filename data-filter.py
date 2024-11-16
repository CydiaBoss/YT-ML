import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Constants
MULT_CSV = False
filepath = "data.csv"
filepath_2 = "data_2.csv"
filepath_final = "data-filtered.csv"
lang = "en"

# Read Data
df = pd.read_csv(filepath, index_col="yt-id")

# Merge multiple if needed
if MULT_CSV:
	df_2 = pd.read_csv(filepath_2, index_col="yt-id")
	df = pd.concat([df, df_2])

print(f"{df.size} rows in data file")

# Remove duplicates
df = df[~df.index.duplicated(keep='first')]
print(f"{df.size} rows remaining after duplication filter")

# Remove non language
def lang_filter(row) -> bool:
	try:
		print(row["title"])
		return detect(row["title"]) == lang
	except LangDetectException:
		return False
	
df = df[df.apply(lang_filter, axis=1)]
print(f"{df.size} rows remaining after translation filter")

# Save Filtered Data
df.to_csv(filepath_final)