from typing import Optional

from pydantic import BaseModel


class Song(BaseModel):
    name: str
    year: int
    artist: str
    shortname: Optional[str]
    bpm: Optional[int]
    duration: Optional[int]
    genre: Optional[str]
    spotifyid: Optional[str]
    album: Optional[str]
