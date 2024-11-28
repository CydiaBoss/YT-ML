import requests
import pandas as pd
import os

# Constants
filepath = "data-filtered.csv"
dirpath = "thumbnail"

# Grab data
df = pd.read_csv(filepath, index_col="yt-id")

# Make directory for image if not already
if not os.path.isdir(dirpath):
	os.mkdir(dirpath)

# Iterate thru dataframe and download
def grab_thumbnail(x : pd.Series):
	# Check if file exist
	filename = f'{dirpath}/{x.name}.jpg'
	if os.path.isfile(filename):
		print(f"Thumbnail already retrieved for {x.name}")
		return

	# Call file
	with open(filename, 'wb') as handle:
		print(f"Retrieving thumbnail for {x.name}")
		response = requests.get(x["thumbnail"], stream=True)

		# Fail request
		if not response.ok:
			print(f"Could not retrieve thumbnail for {x.name}")

		# Success save
		for block in response.iter_content(1024):
			if not block:
				break

			handle.write(block)

# Apply to all
df.apply(grab_thumbnail, axis=1)