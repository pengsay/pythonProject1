from pydantic import BaseModel
from typing import Optional, List, Dict


class Pools(BaseModel):
    name: str
    partition: Optional[str] = "Common"
    order: Optional[int] = 0
    ratio: Optional[int] = 1


class WideCreate(BaseModel):
    name: str
    pools: List[Pools]
    partition: Optional[str] = "Common"


class NameReference(BaseModel):
    link: Optional[str] = None


class UpdatePool(Pools):
    nameReference: NameReference


class UpdateWideIp(BaseModel):
    pools: List[UpdatePool]
