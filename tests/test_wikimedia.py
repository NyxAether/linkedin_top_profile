# Pytest for WikimediaConnector
import pytest
import yaml
from linkedin_top_profile.paths import Paths
from linkedin_top_profile.wikimedia import WikiCredentials, WikiHeaders, WikimediaConnector

@pytest.fixture
def headers()-> WikiHeaders:
    paths = Paths()
    creds = WikiCredentials.model_validate( yaml.safe_load(paths.wikimedia_credentials.read_text(encoding = "utf-8")) )
    return WikiHeaders.load(creds)

def test_wikimedia_connector(headers: WikiHeaders):
    # Initialize the WikimediaConnector
    connector = WikimediaConnector(headers)

    # Call the get_daily_picture method
    picture = connector.get_daily_picture()
    print(picture)
    # Assert that the picture is not None
    # assert picture is not None