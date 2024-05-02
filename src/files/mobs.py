from pydantic import BaseModel, Field
from typing import Dict


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


list_mobs = [
    class_mob(
        id=0,
        name="Goblin",
        stats={
            "damage": 4,
            "defence": 2,
            "hp_max": 4,
            "hp": 4,
        },
        xp=1,
    ),
    class_mob(
        id=1,
        name="Ogro",
        stats={
            "damage": 5,
            "defence": 3,
            "hp": 5,
            "hp_max": 5,
        },
        xp=3,
    ),
    class_mob(
        id=2,
        name="Ogro con Armadura",
        stats={
            "damage": 7,
            "defence": 4,
            "hp": 7,
            "hp_max": 7,
        },
        xp=10,
    ),
]
