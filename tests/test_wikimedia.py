# Pytest for WikimediaConnector
import pytest
import validators
import yaml

from linkedin_top_profile.paths import Paths
from linkedin_top_profile.wikimedia import (WikiCredentials, WikiHeaders,
                                            WikimediaConnector)


@pytest.fixture
def headers() -> WikiHeaders:
    paths = Paths()
    creds = WikiCredentials.model_validate(
        yaml.safe_load(paths.wikimedia_credentials.read_text(encoding="utf-8"))
    )
    return WikiHeaders.load(creds)


def test_wikimedia_connector(headers: WikiHeaders) -> None:
    # Initialize the WikimediaConnector
    connector = WikimediaConnector(headers)

    # Call the get_daily_picture method
    picture = connector.get_daily_picture()
    assert picture.artist is not None
    assert picture.source is not None
    assert validators.url(picture.source)
    assert picture.license is not None
