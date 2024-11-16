import re
import pandas as pd
from PIL import Image

import nltk
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer, TreebankWordTokenizer

# Constants
filepath = "data-filtered.csv"
file_processed = "data-processed.csv"

# Read Data
df = pd.read_csv(filepath, index_col="yt-id")

# Create new dataframe for processed data
processed_df = df[["title", "view-count"]]

# Remove meaningless words and emoji from title
token = TreebankWordTokenizer()
detoken = TreebankWordDetokenizer()
nltk.download('stopwords')
stopwords_list = stopwords.words("english")

emoji_re = re.compile(pattern="[\U000000A9-\U0010ffff]", flags = re.UNICODE)
def filter_title(x):
	# Remove Emojis
	raw_title = emoji_re.sub(r'', x["title"])

	# Remove insignificant words
	words = token.tokenize(raw_title.lower())
	filter_words = [word for word in words if word not in stopwords_list]
	x["title"] = detoken.detokenize(filter_words)
	return x

processed_df = processed_df.apply(filter_title, axis=1, result_type='broadcast')

processed_df.to_csv(file_processed)