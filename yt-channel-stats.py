import json
import urllib.request
import urllib.error
import string
import random
import os
import pandas as pd

from pprint import pprint
from langdetect import detect


# fetch url
def fetch_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read(), None
    except Exception as e:
        return None, e


# create the api channel search call given query and api key
def create_channel_search_call(q: str, API_KEY: str, pageToken=None,
                               part="snippet", type="channel", 
                               relevanceLanguage="en", maxResults="50"):
    url = f"https://www.googleapis.com/youtube/v3/search?part={part}&q={q}&type={type}&key={API_KEY}&relevanceLanguage={relevanceLanguage}&maxResults={maxResults}"
    if pageToken is None:
        return url 
    else:
        return f"{url}&pageToken={pageToken}"


# get data from "snippet" field of channel list query response, return None if detect non english
def get_channel_id_title(snippet, cols=('channelId', 'channelTitle', 'title')):
    desc = snippet.get('description', '')

    if desc == '' or detect(desc) == 'en':
        return {col: snippet.get(col, '') for col in cols}
    else:
        return None
    

# pull relevant data from channel search call
def clean_channel_search_data(raw_channels_data_dict, id_key='channelId'):
    res = {}
    for channel in raw_channels_data_dict['items']:
        curr_id_title = get_channel_id_title(channel['snippet'])
        if curr_id_title is not None:
            res[curr_id_title[id_key]] = curr_id_title

    return res


# retrieve statistics for channels
def create_channel_stats_call(channel_ids, API_KEY: str, part='statistics'):
    return f"https://youtube.googleapis.com/youtube/v3/channels?part={part}&key={API_KEY}&id={','.join(channel_ids)}"


# gets the sub count, video count and view count of a channel
def get_channel_stats(statistics, cols=('subscriberCount', 'videoCount', 'viewCount')):
    isSubCountHidden = statistics['hiddenSubscriberCount']

    if not isSubCountHidden:
        return {col: statistics.get(col, '') for col in cols}
    else:
        return None


# pull relevant data from channel stats call
def clean_channel_stats_data(raw_channels_data_dict, id_key='channelId'):
    res = {}
    for channel in raw_channels_data_dict['items']:
        curr_id = channel['id']
        curr_stats = get_channel_stats(channel['statistics'])
        if curr_stats is not None:
            res[curr_id] = curr_stats

    return res

# call apis to get channel from search api and related statistics (views/subcount)
def get_combined_channel_data(pageToken, query, API_KEY, save_path):

    channel_search_call = create_channel_search_call(query, API_KEY, pageToken)
    raw_data, error = fetch_url(channel_search_call)
    channels_data = None
    nextPageToken = None
    if error is None:
        channels_data = json.loads(raw_data)
        pprint(channels_data)
        nextPageToken = channels_data['nextPageToken']
        channels_data = clean_channel_search_data(channels_data)
    else:
        raise error

    
    channel_stats_call = create_channel_stats_call(list(channels_data.keys()), API_KEY, part='statistics')
    raw_data, error = fetch_url(channel_stats_call)
    channels_stats_data = None
    if error is None:
        channels_stats_data = json.loads(raw_data)
        pprint(channels_stats_data)
        channels_stats_data = clean_channel_stats_data(channels_stats_data)
    else:
        raise error

    channels_data = pd.DataFrame.from_dict(channels_data, orient='index')
    channels_stats_data = pd.DataFrame.from_dict(channels_stats_data, orient='index')
    
    channels_combined_data = pd.merge(channels_data, channels_stats_data, left_index=True, right_index=True)
    channels_combined_data.to_parquet(f'{save_path}/nextPage_{nextPageToken}.parquet')

    return channels_combined_data, nextPageToken

def main():
    MAX_ITERATIONS = 25
    API_KEY = os.environ.get('APIKEY')
    query = 'chess'
    pageToken = None
    save_path = './chess_channels'

    total_channels_retrieved = 0
    for _ in range(MAX_ITERATIONS):
        try:
            channel_data, pageToken = get_combined_channel_data(pageToken, query, API_KEY, save_path)
            print(f'Pulled data for {len(channel_data)} channels.')
            total_channels_retrieved += len(channel_data)
        except Exception as e:
            print("Likely reached quota limit. Try again later.")
            print(f"Total # of channels pulled: {total_channels_retrieved}")
            print(e)
            break

if __name__ == '__main__':
    main()



