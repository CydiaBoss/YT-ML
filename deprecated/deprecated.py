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

# Tokenizer
tokenizer_layer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer_layer.fit_on_texts(raw_data["title"])
sequences = tokenizer_layer.texts_to_sequences(raw_data["title"])
padded_sequences = pad_sequences(sequences, maxlen=10, padding='post')

# Filter
images = images[valid_index]

# Normalize Pixels
images /= 255.0

# Vectorization Layer
vectorize_layer = TextVectorization(
    standardize=text_standardization,
    max_tokens=text_input_dim,
    output_mode="int",
    output_sequence_length=sequence_length,
)

# Label Processing
scores = raw_data["viewCount"] # Grab View Count
scores = scores.fillna(0.0) # Replace NaN with 0
scores = scores.map(lambda x : np.log10(x + 1)) # Log everything to make it less extreme
scores = scores.div(np.log10(MAX_VIEWS + 1)) # Normalized (+1 to prevent one)

plt.hist(scores, 10)

# Boolean Label
b_scores = scores.map(lambda x : int(x >= THRESHOLD))

plt.pie(b_scores.value_counts(), labels=["Bad", "Good"])