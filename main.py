from gateway import Client
from youtube import LastVideo
from extensions import (
    run_on_low_level,
    say,
)
from tqdm import tqdm

bot = Client()

@run_on_low_level
def youtube_notification(
    id: str,
    discord_channel_id: int,
    api_key: str,
) -> None:
    video = LastVideo(id, api_key)
    last_video = video.last_video_url
    old_last_video = video.old_last_video["new_video"]

    while True:
        bot.wait(30000)

        print("마지막 영상: " + last_video)
        print("이전 마지막 영상: " + old_last_video)

        if last_video != old_last_video:
            print("데이터베이스 업데이트")
            for _ in tqdm(range(1)):
                video.update()
            print("메시지를 보냄.")
            try:
                say(
                    bot.token,
                    discord_channel_id,
                    content="🥬수상한 보리 밭에서 상추가 자라다?!?!?!",
                    components=[
                        dict(
                            type=1,
                            components=[
                                dict(
                                    type=2,
                                    label="이를 클릭하다?!??!",
                                    style=5,
                                    url=last_video
                                )
                            ]
                        )
                    ]
                )
            except Exception as error:
                print(f"오류가 발생함: {error}")

        last_video = video.last_video_url
        old_last_video = video.old_last_video

youtube_notification("UChDbYnv1Y_a1AacHM2u2X7w", 929078892118036480, "A YOUTUBE API TOKEN")
bot.login("A DISCORD BOT TOKEN")
