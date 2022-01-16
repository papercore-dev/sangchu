from gateway import Client
from youtube import LastVideo
from httpx import post
from extensions import run_on_low_level

bot = Client()

@run_on_low_level
def youtube_notification(
    id: str,
    discord_channel_id: int,
    api_key: str,
    token: str
) -> None:
    video = LastVideo(id, api_key)
    last_video = video.last_video_url
    old_last_video = video.old_last_video.get("new_video")

    while True:
        bot.wait(30000)

        print("확인된? %s"%last_video)
        print("새로운 비디오? %s"%old_last_video)

        if last_video != old_last_video:
            video.update()
            request = post(
                "https://discord.com/api/v9/channels/%d/messages"%discord_channel_id,
                headers={
                    "authorization":  "Bot %s"%token,
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
            except Exception as error:
                print("Warning: %s"%error)

        last_video = video.last_video_url
        old_last_video = video.old_last_video

youtube_notification("UChDbYnv1Y_a1AacHM2u2X7w", 929078892118036480, "A YOUTUBE API TOKEN", bot.token)
bot.login("A DISCORD TOKEN")
