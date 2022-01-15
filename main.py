import gateway, youtube, threading, httpx
from logging import basicConfig, INFO; basicConfig(level=INFO)
from typing import TypeVar

bot = gateway.GatewayBot("A BOT TOKEN")
Loop = TypeVar("Loop")

def run_on_low_level(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper

@run_on_low_level
def youtube_notification(_youtube, _discord, _token, _api_key) -> Loop:
    video = youtube.GetLastVideo(_youtube, _api_key)
    
    while True:
        bot._wait(30000)
        last_video = video.last_video_url
        old_last_video = video.old_last_video["new_video"]

        print("확인된: %s"%last_video)
        print("새로운 비디오? %s"%old_last_video)

        if last_video != old_last_video:
            video._update_last_video()
            request = httpx.post(
                "https://discord.com/api/v9/channels/%s/messages"%_discord,
                headers={
                    "authorization":  "Bot %s"%_token,
                    "content-type": "application/json"
                },
                json={
                    "content": "새로운 상추가 자라다?!",
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "label": "이를 클릭하다?",
                                    "style": 5,
                                    "url": last_video
                                }
                            ]
                        }
                    ]
                }
            )
            try:
                request.raise_for_status()
            except Exception as e:
                print("Warning: %s"%e)
        last_video = video.last_video_url

youtube_notification("UChDbYnv1Y_a1AacHM2u2X7w", "929078892118036480", bot.token, "A YOUTUBE API TOKEN")
bot._login()
