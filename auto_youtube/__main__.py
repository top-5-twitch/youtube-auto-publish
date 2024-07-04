from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from asyncio import sleep, run

from auto_youtube.config import settings


class AutoYoutube:
    def __init__(self, username, password) -> None:
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
            EC.presence_of_element_located((By.ID, "password"))
        ).find_element(By.CSS_SELECTOR, "input")
        password_input.send_keys(self.__password)

        next_button_password = self.__wait.until(
            EC.element_to_be_clickable((By.ID, "passwordNext"))
        )
        next_button_password.click()

    async def post_video(self, video_path: str):
        create_button = self.__wait.until(
            EC.element_to_be_clickable((By.ID, "buttons"))
        ).find_element(By.CSS_SELECTOR, "button")
        create_button.click()

    async def post_description(self, video_description: str): ...

    async def post_thumbnail(self, thumbnail_path: str): ...

    def __enter__(self):
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option("useAutomationExtension", False)
        self.__options.add_argument("--disable-blink-features=AutomationControlled")

        self.__browser = Chrome(self.__options)
        self.__wait = WebDriverWait(self.__browser, 10)
        return self

    def __exit__(self, _, __, ___):
        self.__browser.quit()


async def test():
    with AutoYoutube(settings.YOUTUBE_USERNAME, settings.YOUTUBE_PASSWORD) as browser:
        await browser.login()
        await browser.post_video("path")
        await sleep(10)


if __name__ == "__main__":
    run(test())
