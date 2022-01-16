from requests import get
from pymongo import MongoClient
from extensions import DictSerializerMixin

dbclient = MongoClient("A MONGODB URL")["dddd"]["dddd"]

class LastVideo(DictSerializerMixin):
    def __init__(self, id: str, api_key: str, **kwargs):
        __slots__ = ("last_video_url", "old_last_video", "id", "api_key")
        super().__init__(**kwargs)
        self.id = id
        self.api_key = api_key
        self.old_last_video = self.get_old()
        self.last_video_url = self.get()

    def get(self):
        channel = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=%s&maxResults=10&order=date&type=video&key=%s"%(self.id, self.api_key)

        lastVideo = get(channel).json()["items"][0]

        return "https://www.youtube.com/watch?v=%s"%lastVideo["id"]["videoId"]

    def update(self):
        global dbclient
        return dbclient.update_one({"_id": "61e2df1d5b282eb1e1ee12b0"}, {"$set": {"new_video": self.last_video_url}})

    def get_old(self):
        global dbclient
        return dbclient.find_one()
