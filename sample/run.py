import os
from asyncio import run
from traceback import print_exc
from youtube_auto_publish import AutoYoutube


async def test():
    try:
        with AutoYoutube(
            os.environ["YOUTUBE_USERNAME"],
            os.environ["YOUTUBE_PASSWORD"],
            "/usr/bin/chromedriver",
        ) as browser:
            await browser.login()
            await browser.post_video(
                channel_name="top5twitchDesenv",
                video_path="/mnt/downloads/final video.mp4",
                video_description="this is a video description",
                tags=["#overwatch", "#pvp"],
                age_restriction=True,
            )
    except Exception as e:
        print_exc()
        raise e


if __name__ == "__main__":
    run(test())
