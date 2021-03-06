from typing import List

from pydantic import BaseModel


class Member(BaseModel):
    name: str
    address: str
    ratio: int


class Pool(BaseModel):
    name: str
    partition: str
    members: List[Member]
