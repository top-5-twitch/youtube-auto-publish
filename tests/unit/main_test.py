import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from youtube_auto_publish import AutoYoutube


@pytest.fixture
def youtube_auto_publish():
    youtube_auto_publish = AutoYoutube("username", "password")
    youtube_auto_publish._AutoYoutube__browser = MagicMock()
    youtube_auto_publish._AutoYoutube__wait = MagicMock()
    return youtube_auto_publish


@patch("youtube_auto_publish.Chrome")
@patch("youtube_auto_publish.ChromeOptions")
def test_enter(options_mock, browser_mock):
    mock_options = options_mock.return_value
    mock_browser = browser_mock.return_value
    with patch("youtube_auto_publish.sleep", new_callable=AsyncMock):
        with AutoYoutube("username", "password") as context:
            mock_options.add_argument.assert_any_call(
                "--disable-blink-features=AutomationControlled"
            )
            mock_options.add_argument.assert_any_call("--lang=en-US")
            assert context._AutoYoutube__browser == mock_browser
            assert isinstance(context._AutoYoutube__wait, WebDriverWait)


@patch("youtube_auto_publish.Chrome", side_effect=Exception)
@patch("youtube_auto_publish.ChromeOptions")
def test_enter_exception(options_mock, browser_mock):
    with pytest.raises(Exception):
        with AutoYoutube("username", "password"):
            ...


@patch("youtube_auto_publish.Chrome", side_effect=TimeoutException)
@patch("youtube_auto_publish.ChromeOptions")
def test_enter_timeout_exception(options_mock, browser_mock):
    with pytest.raises(TimeoutException):
        with AutoYoutube("username", "password"):
            ...


@patch("youtube_auto_publish.Chrome")
def test_exit(chrome_mock):
    mock_browser = chrome_mock.return_value

    context = AutoYoutube("username", "password")
    context._AutoYoutube__browser = mock_browser

    context.__exit__()

    mock_browser.quit.assert_called_once()


@pytest.mark.asyncio
async def test_login(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__wait.until.side_effect = [
        MagicMock(),  # sign_in_button
        MagicMock(),  # email_input
        MagicMock(),  # next_button
        MagicMock(),  # password_input
        MagicMock(),  # next_button_password
    ]

    with patch("youtube_auto_publish.sleep", new_callable=AsyncMock):
        await youtube_auto_publish.login()

    assert youtube_auto_publish._AutoYoutube__browser.get.called
    assert youtube_auto_publish._AutoYoutube__wait.until.called


@pytest.mark.asyncio
async def test_login_exception(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__wait.until.side_effect = [
        Exception(),  # sign_in_button
    ]

    with pytest.raises(Exception), patch(
        "youtube_auto_publish.sleep", new_callable=AsyncMock
    ):
        await youtube_auto_publish.login()


def test_post_thumbnail(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__post_thumbnail("path/to/thumbnail")

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


def test_post_tags(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__post_tags(["tag1", "tag2"])

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


def test_mark_no_safe_for_kids(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__mark_no_safe_for_kids()

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


def test_mark_age_restricted(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__mark_age_restricted()

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


def test_go_to_publish_page(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__go_to_publish_page()

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


def test_select_publish_video(youtube_auto_publish):
    youtube_auto_publish._AutoYoutube__browser.find_element.return_value = MagicMock()

    youtube_auto_publish._AutoYoutube__select_publish_video()

    assert youtube_auto_publish._AutoYoutube__browser.find_element.called


@pytest.mark.asyncio
async def test_post_video_success():
    instance = AutoYoutube("username", "password")
    instance._AutoYoutube__wait = MagicMock()
    instance._AutoYoutube__wait.until = MagicMock()
    instance._AutoYoutube__wait.until.return_value.click = MagicMock()
    instance._AutoYoutube__post_thumbnail = MagicMock()
    instance._AutoYoutube__mark_no_safe_for_kids = MagicMock()
    instance._AutoYoutube__mark_age_restricted = MagicMock()
    instance._AutoYoutube__post_tags = MagicMock()
    instance._AutoYoutube__go_to_publish_page = MagicMock()
    instance._AutoYoutube__select_publish_video = MagicMock()

    with patch("youtube_auto_publish.sleep", new_callable=AsyncMock):
        result = await instance.post_video(
            channel_name="Test Channel",
            video_path="path/to/video",
            tags=["tag1", "tag2"],
            video_description="Test Description",
            thumbnail_path="path/to/thumbnail",
            age_restriction=True,
        )

    assert result is True


@pytest.mark.asyncio
async def test_post_video_success_no_optional():
    instance = AutoYoutube("username", "password")
    instance._AutoYoutube__wait = MagicMock()
    instance._AutoYoutube__wait.until = MagicMock()
    instance._AutoYoutube__wait.until.return_value.click = MagicMock()
    instance._AutoYoutube__mark_no_safe_for_kids = MagicMock()
    instance._AutoYoutube__go_to_publish_page = MagicMock()
    instance._AutoYoutube__select_publish_video = MagicMock()

    with patch("youtube_auto_publish.sleep", new_callable=AsyncMock):
        result = await instance.post_video(
            channel_name="Test Channel",
            video_path="path/to/video",
            video_description="Test Description",
        )

    assert result is True


@pytest.mark.asyncio
async def test_post_video_exception():
    instance = AutoYoutube("username", "password")
    instance.__wait = MagicMock()
    instance.__wait.until.side_effect = Exception("Test Exception")

    with patch("traceback.print_exc", MagicMock()):
        result = await instance.post_video(
            channel_name="Test Channel", video_path="path/to/video"
        )

    assert result is False
