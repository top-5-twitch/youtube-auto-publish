import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from selenium.webdriver.support.ui import WebDriverWait
from auto_youtube import AutoYoutube


@pytest.fixture
def auto_youtube():
    auto_youtube = AutoYoutube("username", "password")
    auto_youtube._AutoYoutube__browser = MagicMock()
    auto_youtube._AutoYoutube__wait = MagicMock()
    return auto_youtube


@patch("auto_youtube.Chrome")
@patch("auto_youtube.ChromeOptions")
def test_enter(options_mock, browser_mock):
    mock_options = options_mock.return_value
    mock_browser = browser_mock.return_value

    with AutoYoutube("username", "password") as context:
        mock_options.add_experimental_option.assert_any_call(
            "excludeSwitches", ["enable-automation"]
        )
        mock_options.add_experimental_option.assert_any_call(
            "useAutomationExtension", False
        )
        mock_options.add_argument.assert_called_with(
            "--disable-blink-features=AutomationControlled"
        )
        assert context._AutoYoutube__browser == mock_browser
        assert isinstance(context._AutoYoutube__wait, WebDriverWait)


@patch("auto_youtube.Chrome")
def test_exit(chrome_mock):
    mock_browser = chrome_mock.return_value

    context = AutoYoutube("username", "password")
    context._AutoYoutube__browser = mock_browser

    context.__exit__()

    mock_browser.quit.assert_called_once()


@pytest.mark.asyncio
async def test_login(auto_youtube):
    auto_youtube._AutoYoutube__wait.until.side_effect = [
        MagicMock(),  # sign_in_button
        MagicMock(),  # email_input
        MagicMock(),  # next_button
        MagicMock(),  # password_input
        MagicMock(),  # next_button_password
    ]

    with patch("auto_youtube.sleep", new_callable=AsyncMock):
        await auto_youtube.login()

    assert auto_youtube._AutoYoutube__browser.get.called
    assert auto_youtube._AutoYoutube__wait.until.called


def test_post_thumbnail(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__post_thumbnail("path/to/thumbnail")

    assert auto_youtube._AutoYoutube__browser.find_element.called


def test_post_tags(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__post_tags(["tag1", "tag2"])

    assert auto_youtube._AutoYoutube__browser.find_element.called


def test_mark_no_safe_for_kids(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__mark_no_safe_for_kids()

    assert auto_youtube._AutoYoutube__browser.find_element.called


def test_mark_age_restricted(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__mark_age_restricted()

    assert auto_youtube._AutoYoutube__browser.find_element.called


def test_go_to_publish_page(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__go_to_publish_page()

    assert auto_youtube._AutoYoutube__browser.find_element.called


def test_select_publish_video(auto_youtube):
    auto_youtube._AutoYoutube__browser.find_element.return_value = MagicMock()

    auto_youtube._AutoYoutube__select_publish_video()

    assert auto_youtube._AutoYoutube__browser.find_element.called


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

    with patch("auto_youtube.sleep", new_callable=AsyncMock):
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

    with patch("auto_youtube.sleep", new_callable=AsyncMock):
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
