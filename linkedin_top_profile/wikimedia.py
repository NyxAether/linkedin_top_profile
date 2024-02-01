import datetime

import requests
from pydantic import BaseModel


class WikiCredentials(BaseModel):
    app_name: str
    email: str
    token: str


class WikiHeaders(BaseModel):
    Authorization: str
    User_Agent: str

    @classmethod
    def load(cls, creds: WikiCredentials) -> "WikiHeaders":
        return cls(
            Authorization=f"Bearer {creds.token}",
            User_Agent=f"{creds.app_name} )({creds.email})",
        )


class WikimediaConnector:
    def __init__(self, headers: WikiHeaders):
        self.headers = headers

    def get_daily_picture(self) -> None:

        today = datetime.datetime.now()
        date = today.strftime("%Y/%m/%d")

        url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + date
        response = requests.get(url, headers=self.headers.model_dump())
        data = response.json()
        print(data)
