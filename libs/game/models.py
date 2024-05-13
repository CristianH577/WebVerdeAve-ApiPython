from pydantic import BaseModel, Field
from typing import Dict


class class_item(BaseModel):
    id: int
    name: str
    kind: str
    effect: list
    desc: str
    quantity: int


class class_mob(BaseModel):
    id: int
    name: str
    stats: Dict[str, int] = Field(
        default={
            "damage": 1,
            "defence": 1,
            "hp": 1,
            "hp_max": 1,
        }
    )
    xp: int


class class_char(BaseModel):
    id: int
    name: str
    clase: str
    stats: Dict[str, int] = Field(
        default={
            "damage": 1,
            "defence": 1,
            "hp": 1,
            "hp_max": 1,
        }
    )
    xp: int = Field(default=0)
    level: int = Field(default=1)
    inventory: Dict[int, class_item] = Field(default={})
    map: dict = Field(
        default={
            "a": {1: {"kind": "wall"}},
            "b": {1: {"kind": "empty"}},
            "c": {1: {"kind": "wall"}},
        }
    )
    effects: dict = Field(default={})
    loc: list = Field(default=["a", 1])
    mob: dict = Field(default={})
