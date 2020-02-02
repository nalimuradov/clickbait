import json
import urllib.request
from train import video_data

api_key = r"AIzaSyDmVJu0dTtlKe36VTd2hmywO5pzPpSsGn4"


def get_videos_from_channel(channel_id):
    video_ids = []
    channel_videos = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/search?part=snippet&"
                                            f"channelId={channel_id}&type=video&order=date&maxResults=50&key={api_key}")
    channel_videos_json = json.loads(channel_videos.read())['items']
    for x in channel_videos_json:
        video_ids.append(x['id']['videoId'])
    return video_ids


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
        return self.metadata_info['items'][0]['snippet']['thumbnails']['default']['url']

    def get_view_count(self):
        return self.statistics_info['items'][0]['statistics']['viewCount']

    def get_subscriber_count(self):
        return self.channel_info['items'][0]['statistics']['subscriberCount']

    def get_vid_frequency(self):
        pass


# key: video_id
# value: [title, subs, thumb, views]
videos = video_data.videos_3


def generate_data():
    training_data = {}

    for video in videos:
        vid_data = Video(video)
        training_data[video] = (vid_data.get_video_title().lower(),
                                vid_data.get_subscriber_count(),
                                vid_data.get_thumbnail(),
                                vid_data.get_view_count(),
                                vid_data.get_vid_frequency())

    with open('data.txt', 'w') as outfile:
        json.dump(training_data, outfile, indent=4)
    # save locally
    return training_data


def print_channel_videos():
    print(get_videos_from_channel("UCn8zNIfYAQNdrFRrr8oibKw"))


def main():
    # print_channel_videos()
    generate_data()
    # print(len(videos))


if __name__ == "__main__":
    main()


'''
polymatter: UCgNg3vwj3xt7QOrcIDaHdFg
DW documentary: UCW39zufHfsuGgpLviKh297Q
JRE clips: UCnxGkOGNMqQEUMvroOWps6Q
Payette Forward: UCiIhoHKPMHm0tpga58IBQNQ
TED: UCAuUUnT6oDeKwE6v1NGQxug
Bon Appetit: UCbpMy0Fg74eXXkvxJrtEn3w
jolly: UCOgGAfSUy5LvEyVS_LF5kdw
thesoundproject: UCou6pqxzTSYf8t-ISPmeQQw

vice: UCn8zNIfYAQNdrFRrr8oibKw
FreeDocumentary: UCijcd0GR0fkxCAZwkiuWqtQ
xbox: UCjBp_7RuDBUYbd1LegWEJ8g
LiamThomson: UCU5O8FCtOTI4BWhfHF2LHJw
RTGame: UCRC6cNamj9tYAO6h_RXd5xA
Great Big Story: UCajXeitgFL-rb5-gXI-aG8Q
3D SANAGO: UCd4FmcWIVdWAy0-Q8OJBloQ
Wired: UCftwRNsjfRo08xYE31tkiyw
NASA Video: UC_aP7p621ATY_yAa8jMqUVA
Josephs Machines: UCbNvfx3rYYxEopnRGxfu53Q
Kurzgesagt: UCsXVk37bltHxD1rDPwtNM8Q
'''
