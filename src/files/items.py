from pydantic import BaseModel


class class_item(BaseModel):
    id: int
    name: str
    kind: str
    effect: list
    desc: str
    quantity: int


list_items = [
    class_item(
        id=0, name="Oro", kind="misc", effect=[], desc="Moneda brillante", quantity=0
    ),
    class_item(
        id=1,
        name="Pocion de vida",
        kind="consumible",
        effect=["hp", 1],
        desc="Restaura vida al consumirse",
        quantity=0,
    ),
    class_item(
        id=2,
        name="Pocion de fua",
        kind="consumible",
        effect=["fua", 1],
        desc="Restaura fua al consumirse",
        quantity=0,
    ),
    class_item(
        id=3,
        name="Espada larga",
        kind="arma",
        effect=["damage", 1],
        desc="El tamaño importa a la hora de clavarla",
        quantity=0,
    ),
    class_item(
        id=4,
        name="Baculo magico",
        kind="arma",
        effect=["damage", 1],
        desc="Con este palo puedes liberar mas el fua",
        quantity=0,
    ),
    class_item(
        id=5,
        name="Armadura de cuero",
        kind="armadura",
        effect=[],
        desc="Armadura hecha con piel de zorra",
        quantity=0,
    ),
    class_item(
        id=6,
        name="Tunica",
        kind="armadura",
        effect=[],
        desc="Un pedazo de tela que basta para vestirse",
        quantity=0,
    ),
    class_item(
        id=7, name="Llave", kind="misc", effect=[], desc="Algo debe abrir", quantity=0
    ),
    class_item(
        id=8,
        name="Llave maestra",
        kind="misc",
        effect=[],
        desc="Algo 'maestro' debe abrir",
        quantity=0,
    ),
    class_item(
        id=9,
        name="Antorcha",
        kind="misc",
        effect=["iluminate", 1],
        desc="Un palo con fuego",
        quantity=0,
    ),
    class_item(
        id=10,
        name="Hoja",
        kind="consumible",
        effect=["olor", -1],
        desc="Se puede usar para limpiarse",
        quantity=0,
    ),
    class_item(
        id=11,
        name="Armadura pesada",
        kind="armadura",
        effect=["defence", 1],
        desc="Armadura mas dura que Maradona",
        quantity=0,
    ),
    class_item(
        id=12,
        name="Espada",
        kind="arma",
        effect=[],
        desc="No impresiona pero sirve",
        quantity=0,
    ),
    class_item(
        id=13,
        name="Caca",
        kind="consumible",
        effect=["hp", -1],
        desc="Es lo que es",
        quantity=0,
    ),
    class_item(
        id=14,
        name="Mascara pintada",
        kind="misc",
        effect=[],
        desc="Parece que estar toda escrita. Seran runas magicas?",
        quantity=0,
    ),
]