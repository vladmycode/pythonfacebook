from unittest.mock import mock_open, patch

import pytest
import requests
from pytest_mock import MockerFixture

from src.pythonfacebook.endpoints import Endpoints
from src.pythonfacebook.facebook import Facebook

TEST_PAGE_ID = "test_page_id"
TEST_ACCESS_TOKEN = "test_access_token"
TEST_IMAGE_ID = "test_image_id"
TEST_POST_ID = "test_post_id"
TEST_VIDEO_ID = "test_video_id"
TEST_COMMENT_ID = "test_comment_id"


@pytest.fixture()
def facebook_client() -> Facebook:
    """Fixture to create a Facebook client for testing."""
    return Facebook(page_id=TEST_PAGE_ID, access_token=TEST_ACCESS_TOKEN)


def test_init(facebook_client: Facebook) -> None:
    """Test Facebook client initialization."""
    assert facebook_client.PAGE_ID == TEST_PAGE_ID
    assert facebook_client.ACCESS_TOKEN == TEST_ACCESS_TOKEN
    assert isinstance(facebook_client.endpoints, Endpoints)


def test_make_request_success(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test successful API request."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch("requests.request", return_value=mock_response)

    # Simulate a request
    response = facebook_client._make_request("http://test.endpoint")

    assert response == {"success": True}


def test_make_request_failure(
    mocker: MockerFixture, facebook_client: Facebook, caplog: pytest.LogCaptureFixture
):
    """Test API request failure."""
    mocker.patch(
        "requests.request",
        side_effect=requests.exceptions.RequestException("Test error"),
    )

    # Simulate a request
    response = facebook_client._make_request("http://test.endpoint")

    assert response is None
    assert "Test error" in caplog.text


def test_upload_image_local_file(
    mocker: MockerFixture, facebook_client: Facebook
) -> None:
    """Test image upload with a local file."""
    mocker.patch("os.path.isfile", return_value=True)
    mock_make_request = mocker.patch.object(
        facebook_client, "_make_request", return_value={"id": TEST_IMAGE_ID}
    )

    # Mock open to simulate file opening
    with patch("builtins.open", mock_open(read_data=b"test_image_data")):
        result = facebook_client._upload_image("/path/to/image.jpg")

    assert result == {"id": TEST_IMAGE_ID}
    mock_make_request.assert_called_once()


def test_upload_image_url(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test image upload with a URL."""
    mocker.patch("os.path.isfile", return_value=False)
    mock_make_request = mocker.patch.object(
        facebook_client, "_make_request", return_value={"id": TEST_IMAGE_ID}
    )

    result = facebook_client._upload_image("http://example.com/image.jpg")

    assert result == {"id": TEST_IMAGE_ID}
    mock_make_request.assert_called_once()


def test_create_image_post(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test creating an image post."""
    mocker.patch.object(
        facebook_client, "_upload_image", return_value={"id": TEST_IMAGE_ID}
    )
    mock_make_request = mocker.patch.object(
        facebook_client, "_make_request", return_value={"post_id": TEST_POST_ID}
    )

    result = facebook_client.create_image_post(
        "Test post", ["/path/to/image1.jpg", "/path/to/image2.jpg"]
    )

    assert result == {"post_id": TEST_POST_ID}
    mock_make_request.assert_called_once()


def test_create_video_post(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test creating a video post."""
    # Mock open to simulate file opening
    with patch("builtins.open", mock_open(read_data=b"test_video_data")):
        mock_make_request = mocker.patch.object(
            facebook_client, "_make_request", return_value={"video_id": TEST_VIDEO_ID}
        )

        result = facebook_client.create_video_post(
            "/path/to/video.mp4", title="Test Video", description="Test Description"
        )

    assert result == {"video_id": TEST_VIDEO_ID}
    mock_make_request.assert_called_once()


def test_create_text_post(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test creating a text post."""
    mock_make_request = mocker.patch.object(
        facebook_client, "_make_request", return_value={"post_id": TEST_POST_ID}
    )

    result = facebook_client.create_text_post(
        "Test text post", url="http://example.com"
    )

    assert result == {"post_id": TEST_POST_ID}
    mock_make_request.assert_called_once()


def test_create_comment(mocker: MockerFixture, facebook_client: Facebook) -> None:
    """Test creating a comment."""
    mock_make_request = mocker.patch.object(
        facebook_client, "_make_request", return_value={"comment_id": TEST_COMMENT_ID}
    )
    result = facebook_client.create_comment(TEST_POST_ID, "Test comment")

    assert result == {"comment_id": TEST_COMMENT_ID}
    mock_make_request.assert_called_once()
