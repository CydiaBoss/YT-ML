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