from pathlib import Path

from pydantic import BaseModel


class Paths(BaseModel):
    home_directory: Path = Path.home()
    cache_directory: Path = home_directory / ".cache"
    wikimedia_credentials: Path = cache_directory / "wikimedia" / "credentials.yml"
