import pandas as pd

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer, TreebankWordTokenizer

# Constants
filepath = "data-filtered.csv"
file_processed = "data-processed.csv"
dirpath = "thumbnail"

# Read Data
df = pd.read_csv(filepath, index_col="yt-id")

# Create new dataframe for processed data
processed_df = df[["title",]]

# Remove meaningless words and emoji from title
token = TreebankWordTokenizer()
detoken = TreebankWordDetokenizer()
# Stopwords
nltk.download('stopwords')
stopwords_list = stopwords.words("english")
# Punctuation
punc_list = list(string.punctuation)
punc_list.append("…")
punc_re = re.compile(pattern=f"[{re.escape(string.punctuation)}]", flags = re.UNICODE)
# Emojis
emoji_re = re.compile(pattern="[\U000000A9-\U0010ffff]", flags = re.UNICODE)

def filter_title(x):
	# Remove Emojis
	print(x["title"])
	raw_title = emoji_re.sub(r'', x["title"])

	# Remove Insignificant Words
	words = token.tokenize(raw_title.lower())
	filter_words = [word for word in words if word not in stopwords_list]

	# Remove Punctuation
	punc_words = [word for word in filter_words if word not in punc_list]
	x["title"] = detoken.detokenize(punc_words)
	x["title"] = punc_re.sub(r'', x["title"])

	return x

processed_df = processed_df.apply(filter_title, axis=1, result_type='broadcast')

# Calculate Scoring for each
processed_df["score"] = df["like-count"]/df["view-count"]

# Fill blank scores with zero (0/0)
processed_df["score"] = processed_df["score"].fillna(0.0)

# Save Processed File
processed_df.to_csv(file_processed)