# Auto Youtube lib


## How to run:
```
from youtube_auto_publish.config import settings
from asyncio import run

async def test():
    video_was_send: bool = False
    number_or_trys: int = 0

    while not video_was_send:
        with AutoYoutube(settings.YOUTUBE_USERNAME, settings.YOUTUBE_PASSWORD) as browser:
            await browser.login()
            video_was_send = await browser.post_video(
                channel_name="top5twitchDesenv",
                video_path=r"C:\Users\lucas\Downloads\final video.mp4",
                video_description="this is a video description",
                tags=["#overwatch","#pvp"],
                age_restriction=True,
            )
        numbers_of_trys += 1

        if video_was_send or number_of_trys >= 5:
            break



if __name__ == "__main__":
    run(test())
```