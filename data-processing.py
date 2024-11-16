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
processed_df = df[["title"]]

# Remove meaningless words and emoji from title
token = TreebankWordTokenizer()
detoken = TreebankWordDetokenizer()
nltk.download('stopwords')
stopwords_list = stopwords.words("english")
def filter_title(x):
	words = token.tokenize(x["title"].lower())
	print(x["title"])
	filter_words = [word for word in words if word not in stopwords_list]
	x["title"] = detoken.detokenize(filter_words)
	print(x["title"])
	return x

processed_df.apply(filter_title, axis=1)