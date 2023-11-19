# 2023.11.09  19.00
from googleapiclient.discovery import build
import isodate
import pandas as pd
from datetime import datetime, timedelta
from warnings import simplefilter
simplefilter(action='ignore', category=Warning)

def youtube_auth():
    return build("youtube","v3", developerKey='AIzaSyBzSaapBAb9sfTih5iHefzDeYOtKB8_G7s')

# --------------------------------------------------------------------
def get_channel_stats():

    channel_ids = ['UCP6gIddjSaCl2ChEA_dNd_w','UC9dhVxpRhVS2W9qTtUTV-Jg','UCvHjNXyqMOsFfY7W4VSOH3g','UCEz9c3Qv7mnZcjP4s2_WpMw','UCAfpm3hE3qtHJB59Ebbd23g','UCS25DG93gAImKWm0YY-IQmQ','UC6IUish1nuhvf2GCyYJPIoQ',
    'UCsjvWMtSQBi2dXak38E-TRg','UCRGDQl_wTmDbPbHCmOia9Kg','UC-NKm49KlQcbVSSr0O2CLzA','UC-4kpl1DLewe0IB7TYLqXxg','UCEPkQCsLHXDq2KLcUvkL_Bg',
    'UChLf4L6Gi0MX-me7NAk5PGg','UC_KaW7yvOgbRID__JSEOcjA','UCXT7EAMTWiWsLgrHFK_Z1mA','UCmSxyKGLy279bPpDGbdOBAA','UCf4MsPw-_lE7LZ_oewH7T2g',
    'UCIyLvX5xxKjo1tZq-yL8rwA','UCTsqeBwD1DD9NdJCx8R5QHg','UCYCOjBOPTnge342C1_ggVMA']

    request = youtube_auth().channels().list(part='snippet,contentDetails,statistics', id=','.join(channel_ids)) #forUsername='schafer5'
    response = request.execute()

    all_data = []
    for i in range(len(response['items'])):
        data = dict(channelName = response['items'][i]['snippet']['title'],
            subscribers = response['items'][i]['statistics']['subscriberCount'],
            views = response['items'][i]['statistics']['viewCount'],
            totalVideos = response['items'][i]['statistics']['videoCount'],
            playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    youtube_channel_df = pd.DataFrame(all_data)
    numeric_cols = ['subscribers', 'views', 'totalVideos']
    youtube_channel_df[numeric_cols] = youtube_channel_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return youtube_channel_df

# --------------------------------------------------------------------
def get_video_ids(playlist_id):

    request = youtube_auth().playlistItems().list(part='contentDetails', playlistId = playlist_id, maxResults = 50)
    response = request.execute()
    
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube_auth().playlistItems().list(part='contentDetails',playlistId = playlist_id, maxResults = 50, pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids[:100]

# --------------------------------------------------------------------
def get_video_details(video_ids):   
    video_info = []  
    for i in range(0, len(video_ids), 50):
        request = youtube_auth().videos().list(part="snippet,contentDetails,statistics",id=','.join(video_ids[i:i+50]))
        response = request.execute() 
        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']  }
            vid_info = {}
            vid_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        vid_info[v] = video[k][v]
                    except:
                        vid_info[v] = None

            video_info.append(vid_info)
    
    video_df = pd.DataFrame(video_info)
    video_df = video_df.drop(['video_id'], axis=1)
    video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds())
    video_df['title'] = video_df['title'].str[:50]
    video_df['publishedDate'] = video_df['publishedAt'].apply(lambda x: isodate.parse_datetime(x)).dt.tz_localize(None) #NoTimezone: dt.tz_localize(None)
    video_df = video_df.drop(['publishedAt', 'duration'], axis=1)

    ncols = ['viewCount', 'likeCount', 'commentCount']
    video_df[ncols] = video_df[ncols].apply(pd.to_numeric, errors='coerce')
          
    return video_df

# --------------------------------------------------------------------
def get_video_comments(video_ids):
    all_comments = []
    for video_id in video_ids:
        try:   
            request = youtube_auth().commentThreads().list( part="snippet,replies",videoId=video_id)
            response = request.execute()
            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:2]]
            comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}
            all_comments.append(comments_in_video_info)  
        except: 
            print('Could not get comments for video ' + video_id) # most likely because comments are disabled on a video
        
    return pd.DataFrame(all_comments)     

# --------------------------------------------------------------------
'''
channel_df = get_channel_stats(channel_ids)
def save_all_videoinfos(filename):
    all_videos_df = pd.DataFrame()
    for yname in channel_df['channelName']: #.unique()
        print("Getting video information from channel: " + yname)
        playlist_id = channel_df.loc[channel_df['channelName']== yname, 'playlistId'].iloc[0]
        video_ids = get_video_ids(playlist_id)
        video_data = get_video_details(video_ids)
        all_videos_df = all_videos_df.append(video_data, ignore_index=True)

    return all_videos_df.to_csv(filename, encoding='utf-8', index=False)

save_all_videoinfos('all_youtube_videos.csv')
'''

'''
file_UnixmodDate = os.path.getmtime('Data_files/all_youtube_videos.csv')
file_modDate = datetime.fromtimestamp(file_UnixmodDate)
print(file_modDate)
checkDate = datetime.now() - timedelta(days = 0.5)
print(checkDate)

if (file_modDate < checkDate):
    print('File need to update')
    save_all_videoinfos('Data_files/all_youtube_videos.csv')
else:
    print('File is uptodate')

print('---------------')
df = pd.read_csv('Data_files/all_youtube_videos.csv')
print(df)
'''


