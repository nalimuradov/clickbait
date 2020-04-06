import json
import urllib.request
from train.data import video_ids

def date_diff(date_recent, date_oldest):
    year_recent, month_recent, day_recent = int(date_recent[0:4]), int(date_recent[5:7]), int(date_recent[8:10])
    year_oldest, month_oldest, day_oldest = int(date_oldest[0:4]), int(date_oldest[5:7]), int(date_oldest[8:10])
    return 365 * (year_recent - year_oldest) + 30 * (month_recent - month_oldest) + (day_recent - day_oldest)


def get_videos_from_channel(channel_id):
    video_id_list = []
    channel_videos = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/search?part=snippet&"
                                            f"channelId={channel_id}&type=video&order=date&maxResults=50&key={api_key}")
    channel_videos_json = json.loads(channel_videos.read())['items']
    for x in channel_videos_json:
        video_id_list.append(x['id']['videoId'])
    return video_id_list


class Channel:
    def __init__(self, channel_id):
        channel_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}" \
                      f"&type=video&order=date&maxResults=50&key={api_key}"
        channel_url = urllib.request.urlopen(channel_url)
        channel_videos_json = json.loads(channel_url.read())['items']


class Video:
    def __init__(self, video_id):
        metadata_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        statistics_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"
        metadata_url = urllib.request.urlopen(metadata_url)
        statistics_url = urllib.request.urlopen(statistics_url)

        self.metadata_info = json.loads(metadata_url.read())
        self.statistics_info = json.loads(statistics_url.read())

        channel_id = self.metadata_info['items'][0]['snippet']['channelId']
        channel_url = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id="
                                             f"{channel_id}&key={api_key}")

        self.channel_info = json.loads(channel_url.read())

    def get_video_title(self):
        return self.metadata_info["items"][0]["snippet"]["title"]

    def get_thumbnail(self):
        return self.metadata_info['items'][0]['snippet']['thumbnails']['high']['url']

    def get_view_count(self):
        return self.statistics_info['items'][0]['statistics']['viewCount']

    def get_subscriber_count(self):
        return self.channel_info['items'][0]['statistics']['subscriberCount']

    # days for 50 uploads
    def get_vid_frequency(self):
        pass
    

def generate_data():
    training_data = {}

    for video in videos:
        vid_data = Video(video)
        training_data[video] = (vid_data.get_video_title().lower(),
                                vid_data.get_subscriber_count(),
                                vid_data.get_thumbnail(),
                                vid_data.get_view_count())

    with open('data.txt', 'w') as outfile:
        json.dump(training_data, outfile, indent=4)
    # save locally
    return training_data


# data generation: find channel -> print video ids -> append to video_ids.py -> extract from there
def main():
    # print_channel_videos()
    generate_data()


if __name__ == "__main__":
    main()
