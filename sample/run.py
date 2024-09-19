import os
from asyncio import run
from youtube_auto_publish import AutoYoutube


async def test():
    print("Starting drive.")
    with AutoYoutube(
        os.environ["YOUTUBE_USERNAME"],
        os.environ["YOUTUBE_PASSWORD"],
    ) as browser:
        print("Login")
        await browser.login()
        print("Post video")
        await browser.post_video(
            channel_name="top5twitchDesenv",
            video_path="/mnt/downloads/final video.mp4",
            video_description="this is a video description",
            tags=["#overwatch", "#pvp"],
            age_restriction=True,
        )

    return True


if __name__ == "__main__":
    run(test())
