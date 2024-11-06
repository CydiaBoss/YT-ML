import json
import urllib.request
import urllib.error
import string
import random
import os
import pandas as pd
from dotenv import load_dotenv

# Load .env file with your api key
load_dotenv()

# Variables
count = 50
max_iterations = 100 # 50 * 100 = 5000 videos
topic_id = "/m/03hf_rm" # Strategy Games
API_KEY = os.getenv("APIKEY")

# Read local data file
filepath = "data.csv"
if os.path.isfile(filepath):
    df = pd.read_csv(filepath, index_col="yt-id")
else:
    df = pd.DataFrame([], columns=["yt-id", "title", "created", "channel-id", "thumbnail", "thumbnail-w", "thumbnail-h", "view-count", "like-count", "comment-count", "query"])
    df = df.set_index("yt-id")

# Loop
yt_reads = 0
for i in range(max_iterations):
    # Generates random query for YT
    r_q = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    # Calls the API for search results (100 units)
    try:
        urlData_query = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&topicId={topic_id}&q={r_q}"
        webURL_query = urllib.request.urlopen(urlData_query)
        raw_vid_data = webURL_query.read()
        results_vids = json.loads(raw_vid_data.decode(webURL_query.info().get_content_charset('utf-8')))

        # Process Video Response
        yt_ids = []
        for video_data in results_vids['items']:
            # Ignore Live and Upcoming Content (no ratings yet)
            if video_data['snippet']['liveBroadcastContent'] != "none":
                continue

            # Parse data
            try:
                new_row = pd.DataFrame([{
                    "yt-id": video_data['id']['videoId'],
                    "title": video_data['snippet']['title'],
                    "created": video_data['snippet']['publishedAt'],
                    "channel-id": video_data['snippet']['channelId'],
                    "thumbnail": video_data['snippet']['thumbnails']["default"]["url"],
                    "thumbnail-w": video_data['snippet']['thumbnails']["default"]["width"],
                    "thumbnail-h": video_data['snippet']['thumbnails']["default"]["height"],
                    "query": r_q,
                },])
                new_row = new_row.set_index("yt-id")

                try:
                    # Append
                    df = pd.concat([df, new_row], verify_integrity=True)

                    # Store your ids
                    yt_reads += 1

                    # Prepare id for stats query
                    yt_ids.append(video_data['id']['videoId'])
                except ValueError:
                    # Duplicate video detected
                    continue
            except KeyError:
                # Weird Entry
                continue

        # Generate & call statistic query (1 unit)
        urlData_stats = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&part=statistics&id={','.join(yt_ids)}"
        webURL_stats = urllib.request.urlopen(urlData_stats)
        raw_stats_data = webURL_stats.read()
        results_stats = json.loads(raw_stats_data.decode(webURL_stats.info().get_content_charset('utf-8')))

        # Process Stats Response
        for stats_data in results_stats["items"]:
            try:
                # Parse data
                new_row = pd.DataFrame([{
                    "yt-id": stats_data['id'],
                    "view-count": stats_data['statistics']['viewCount'],
                    "like-count": stats_data['statistics']['likeCount'] if 'likeCount' in stats_data['statistics'] else "",
                    "comment-count": stats_data['statistics']['commentCount'] if 'commentCount' in stats_data['statistics'] else "",
                },])
                new_row = new_row.set_index("yt-id")

                # Update main dataset
                df.update(new_row)
            except KeyError:
                # Weird Entry
                continue

        # Update User
        print(f"API call #{i} successfully")

        # Dumb Data to prevent loss every 5 runs
        if i % 5 == 0:
            df.to_csv(filepath)

    # ON API failure, quit and save
    except urllib.error.HTTPError:
        print("Latest API call failed. You are likely out of units. Try again tomorrow.")
        break
    
# Write to csv
df.to_csv(filepath)

# Termination
print(f"Was able to pull {yt_reads} rows")