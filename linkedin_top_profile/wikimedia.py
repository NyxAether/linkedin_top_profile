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


class ArtistInfos(BaseModel):
    text: str


class SourceInfos(BaseModel):
    source: str


class LicenceInfos(BaseModel):
    code: str


class ImageInfos(BaseModel):
    title: str
    artist: ArtistInfos
    image: SourceInfos
    license: LicenceInfos


class WikiJson(BaseModel):
    image: ImageInfos


class PictureOfDay(BaseModel):
    title: str
    artist: str
    source: str
    license: str

    @classmethod
    def load(cls, data: WikiJson) -> "PictureOfDay":
        infos = {}
        infos["title"] = data.image.title
        infos["artist"] = data.image.artist.text
        infos["source"] = data.image.image.source
        infos["license"] = data.image.license.code
        return cls(**infos)


class WikimediaConnector:
    def __init__(self, headers: WikiHeaders):
        self.headers = headers

    def get_daily_picture(self) -> PictureOfDay:

        today = datetime.datetime.now()
        date = today.strftime("%Y/%m/%d")

        url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + date
        response = requests.get(url, headers=self.headers.model_dump())
        infos = WikiJson.model_validate(response.json())
        return PictureOfDay.load(infos)
