from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from asyncio import sleep, run

from auto_youtube.config import settings


class AutoYoutube:
    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        self.__username = username
        self.__password = password
        self.__browser: Chrome
        self.__options = ChromeOptions()
        self.__wait: WebDriverWait

    async def login(self) -> None:
        self.__browser.get("https://youtube.com")

        sign_in_button = self.__wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Fazer login"))
        )
        sign_in_button.click()

        email_input = self.__wait.until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(self.__username)

        next_button = self.__wait.until(
            EC.element_to_be_clickable((By.ID, "identifierNext"))
        )
        next_button.click()

        password_input = self.__wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password input"))
        )
        password_input.send_keys(self.__password)

        next_button_password = self.__wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#passwordNext button"))
        )

        await sleep(3)
        next_button_password.click()

    async def post_video(
        self,
        channel_name: str,
        video_path: str,
        tags: list[str] = [],
        video_description: str = "",
        thumbnail_path: str = "",
    ):
        channel_button = self.__wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[@id='channel-title' and text()='{channel_name}']")
            )
        )
        channel_button.click()

        await sleep(3)

        create_button = self.__wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Create']"))
        )
        create_button.click()

        upload_video_button = self.__wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='label' and text()='Upload video']")
            )
        )
        upload_video_button.click()

        upload_arrow_button = self.__wait.until(
            EC.presence_of_element_located((By.ID, "content"))
        ).find_element(By.CSS_SELECTOR, "input")

        upload_arrow_button.send_keys(video_path)

        await sleep(3)

        description_box = self.__wait.until(
            EC.presence_of_element_located((By.ID, "description-wrapper"))
        ).find_element(By.ID, "textbox")

        description_box.send_keys(video_description)

        if thumbnail_path:
            thumbnail_button = self.__browser.find_element(By.ID, "select-button")

            thumbnail_button.send_keys(thumbnail_path)

        not_for_kids_button = self.__browser.find_element(
            By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK"
        ).find_element(By.ID, "radioLabel")

        not_for_kids_button.click()

        if tags:
            show_more_button = self.__browser.find_element(By.ID, "toggle-button")

            show_more_button.click()

            tags_input_box = self.__browser.find_element(
                By.ID, "tags-container"
            ).find_element(By.ID, "text-input")

            tags_input_box.send_keys(", ".join(tags))

        next_button = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button.click()

        next_button = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button.click()

        next_button = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button.click()

        public_button = self.__browser.find_element(
            By.XPATH, "//div[@id='radioLabel' and text()='Public']"
        )

        public_button.click()

        await sleep(5)

        publish_button = self.__wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='done-button' and @aria-disabled='false']"),
            )
        )

        publish_button.click()

    def __enter__(self):
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option("useAutomationExtension", False)
        self.__options.add_argument("--disable-blink-features=AutomationControlled")

        self.__browser = Chrome(self.__options)
        self.__wait = WebDriverWait(self.__browser, 10)
        return self

    def __exit__(self, *args):
        self.__browser.quit()


async def test():
    with AutoYoutube(settings.YOUTUBE_USERNAME, settings.YOUTUBE_PASSWORD) as browser:
        await browser.login()
        await browser.post_video(
            channel_name="top5twitchDesenv",
            video_path=r"C:\Users\lucas\Downloads\final video.mp4",
            video_description="this is a video description",
            tags=["#overwatch"],
        )
        await sleep(10)


if __name__ == "__main__":
    run(test())
