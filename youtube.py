import httpx, re
from pymongo import MongoClient
from typing import TypeVar
from warnings import warn

YouTubeChannel = TypeVar("YouTubeChannel")
dbclient = MongoClient("A MONGODB URL")["dddd"]["dddd"]

class DictSerializerMixin(object):
    def __init__(self, **d):
        __slots__ = "_kwds"
        self._kwds = d

        for key in d:
            if key in self.__slots__ if hasattr(self, "__slots__") else True:
                self.__setattr__(key, d[key])
            else:
                warn("Missing key '%s' from class %s"%(key, self.__class__.__name__))

        if hasattr(self, "__slots__"):
            for attr in self.__slots__:
                if not hasattr(self, attr):
                    self.__setattr__(attr, None)

class GetLastVideo(DictSerializerMixin):
    def __init__(self, id: YouTubeChannel, api_key: str, **kwargs):
        __slots__ = ("last_video_url", "old_last_video", "dbclient", "id", "api_key")
        super().__init__(**kwargs)
        self.id = id
        self.api_key = api_key
        self.old_last_video = self._get_old_last_video()
        self.last_video_url = self._get_last_video()

    def _get_last_video(self) -> YouTubeChannel:
        channel = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=%s&maxResults=10&order=date&type=video&key=%s"%(self.id, self.api_key)

        lastVideo = httpx.get(channel).json()["items"][0]

        return "https://www.youtube.com/watch?v=%s"%lastVideo["id"]["videoId"]

    def _update_last_video(self) -> YouTubeChannel:
        global dbclient
        return dbclient.update_one({"_id": "MONGODB OBJECT ID"}, {"$set": {"new_video": self.last_video_url}})

    def _get_old_last_video(self) -> YouTubeChannel:
        global dbclient
        return dbclient.find_one()
