from libs.game.models import class_item


levels = {
    1: range(3),
    2: range(4, 7),
    3: range(8, 13),
    4: range(14, 23),
}

test_char_data = {
    "id": 2,
    "name": "kolimba",
    "clase": "warrior",
    "stats": {
        "damage": 99,
        "defence": 3,
        "hp": 4,
        "hp_max": 4,
    },
    "effects":{"damage":1},
    "inventory": {
        3: class_item(
            id=3,
            name="Espada larga",
            kind="arma",
            effect=["damage", 1],
            desc="El tamaño importa a la hora de clavarla",
            quantity=1,
        ),
        5: class_item(
            id=5,
            name="Armadura de cuero",
            kind="armadura",
            effect=[],
            desc="Armadura hecha con piel de zorra",
            quantity=1,
        ),
        # 9: class_item(
        #     id=9,
        #     name="Antorcha",
        #     kind="misc",
        #     effect=["iluminate", 1],
        #     desc="Un palo con fuego",
        #     quantity=99,
        # ),
    },
}
admin_char_data = {
    "id": 1,
    "name": "kolimba admin",
    "clase": "warrior",
    "stats": {
        "damage": 99,
        "defence": 3,
        "hp": 3,
        "hp_max": 4,
    },
    "inventory": {
        3: class_item(
            id=3,
            name="Espada larga",
            kind="arma",
            effect=["damage", 1],
            desc="El tamaño importa a la hora de clavarla",
            quantity=1,
        ),
        5: class_item(
            id=5,
            name="Armadura de cuero",
            kind="armadura",
            effect=[],
            desc="Armadura hecha con piel de zorra",
            quantity=1,
        ),
        1: class_item(
            id=1,
            name="Pocion de vida",
            kind="consumible",
            effect=["hp", 1],
            desc="Restaura vida al consumirse",
            quantity=1,
        ),
        8: class_item(
            id=8,
            name="Llave maestra",
            kind="misc",
            effect=[],
            desc="Algo 'maestro' debe abrir",
            quantity=1,
        ),
        7: class_item(
            id=7,
            name="Llave",
            kind="misc",
            effect=[],
            desc="Algo debe abrir",
            quantity=1,
        ),
    },
    "map": {
        "a": {1: {"kind": "wall"}},
        "b": {1: {"kind": "empty"}},
        "c": {1: {"kind": "wall"}},
    },
}
