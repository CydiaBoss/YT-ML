# This file will hold deprecated cells that are no longer used

# Image Processing Cell
files = [f for f in os.listdir(dirpath) if os.path.isfile(f"{dirpath}/{f}") and f.endswith(".jpg")]
images = np.zeros((len(files), 90, 120, 3))
image_ids = []
valid_index = []
i = 0
for f in files:
	try:
		im = Image.open(f"{dirpath}/{f}")
		images[i] = np.array(im)
		image_ids.append(f[:-4])
		im.close()

		# Save valid indexes for filtering
		valid_index.append(i)
	except:
		pass

	i += 1

# Filter
images = images[valid_index]

# Normalize Pixels
images /= 255.0

# Regex Patterns
emoji_re = "[\U000000A9-\U0010ffff]"
punc_re = f"[{re.escape(string.punctuation)}]"
space_re = "\s{1,}"

# Download Stopwords & pattern
nltk.download('stopwords')
stopwords_list = stopwords.words("english")
sw_re = f'\b(?:{"|".join([f"{re.escape(sw)}" for sw in stopwords_list])})\b'

# Text Processing
def text_standardization(raw_strs):
	t = tf.strings.lower(raw_strs)
	t = tf.strings.regex_replace(t, emoji_re, "")
	t = tf.strings.regex_replace(t, sw_re, "")
	t = tf.strings.regex_replace(t, punc_re, "")
	t = tf.strings.regex_replace(t, space_re, " ")
	return t

# Vectorization Layer
vectorize_layer = TextVectorization(
    standardize=text_standardization,
    max_tokens=text_input_dim,
    output_mode="int",
    output_sequence_length=sequence_length,
)