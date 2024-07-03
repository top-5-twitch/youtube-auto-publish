from selenium.webdriver.common.by import By
from asyncio import sleep, run
from auto_youtube.web_browser import MakeBrowser
from auto_youtube.config import settings


class Main:
    @staticmethod
    async def run():
        with MakeBrowser() as browser:
            browser.get("https://youtube.com")

            await sleep(3)

            sign_in_button = browser.find_element(By.LINK_TEXT, "Fazer login")
            sign_in_button.click()

            await sleep(3)

            email_input = browser.find_element(By.ID, "identifierId")
            email_input.send_keys(settings.YOUTUBE_USERNAME)

            next_button = browser.find_element(By.ID, "identifierNext")
            next_button.click()

            await sleep(3)

            password_input = browser.find_element(
                By.CSS_SELECTOR, "input[type='password']"
            )
            password_input.send_keys(settings.YOUTUBE_PASSWORD)

            next_button = browser.find_element(By.ID, "passwordNext")
            next_button.click()

            await sleep(10)


# browser.quit
if __name__ == "__main__":
    run(Main.run())
