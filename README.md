# ML YT Model
This model will take a YT video's thumbnail and title as an input and return it's performance in some metric as its output.

# Setup
Run this command to install pandas
```
pip install pandas
```
Then make a `.env` file in the same directory with one variable
```
APIKEY=your-api-key-here
```
Then, simply run the `yt-crawler.py` to pull data from the YT APIs for training and testing data