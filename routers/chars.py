from fastapi import APIRouter, HTTPException, Form

from pydantic import BaseModel, Field
from typing import Annotated, Union, Dict

from json import loads
import copy

from src.files.map import map
from src.files.mobs import list_mobs
from src.files.items import class_item, list_items


# configs ----------------------------------------------------------------------
router = APIRouter(
    prefix="/chars", tags=["chars"], responses={404: {"error": "error router chars"}}
)


# consts  ----------------------------------------------------------------------
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

list_class_default = [admin_char_data, test_char_data]
list_class = [class_char(**admin_char_data), class_char(**test_char_data)]


# functions --------------------------------------------------------------------------------
def searchCharDefaultById(id: int):
    e = filter(lambda x: x["id"] == id, list_class_default)
    e = list(e)[0]
    try:
        return copy.deepcopy(e)
    except:
        raise HTTPException(status_code=404, detail="personaje default no encontrado")


def searchCharById(id: int):
    e = filter(lambda x: x.id == id, list_class)
    e = list(e)[0]
    try:
        return copy.deepcopy(e)
    except:
        raise HTTPException(status_code=404, detail="personaje no encontrado")


def searchChar(filters: dict):
    def Filt(x):
        found = False
        dic_x = x.dict()
        keys = list(dic_x.keys())
        for k, v in filters.items():
            if not v in (0, "") and k in keys:
                if v == dic_x[k]:
                    found = True
                else:
                    found = False
                    break
        return found

    e = filter(Filt, list_class)
    e = list(e)
    try:
        return copy.deepcopy(e)
    except:
        raise HTTPException(status_code=404, detail="no encontrado")


def searchItemById(id: int):
    e = filter(lambda x: x.id == id, list_items)
    e = list(e)[0]
    try:
        return copy.deepcopy(e)
    except:
        raise HTTPException(status_code=404, detail="item no encontrado")


def searchMobById(id: int):
    e = filter(lambda x: x.id == id, list_mobs)
    e = list(e)[0]
    try:
        return copy.deepcopy(e)
    except:
        raise HTTPException(status_code=404, detail="mob no encontrado")


async def updateChar(char: class_char):
    found = False

    for i, x in enumerate(list_class):
        if x.id == char.id:
            list_class[i] = char
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="no existe")


def updateMapAll(char: class_char):
    if not char:
        raise HTTPException(status_code=404, detail="no char")

    if isinstance(char, int):
        char = searchCharById(char)

    cols = list(map["base"].keys())
    for col in cols:
        char.map[col] = {}
        for row in range(1, 22):
            kind = map["base"][col][row]

            char.map[col][row] = {
                "kind": kind,
            }

            if kind == "empty":
                try:
                    door = map["doors"][col, row]
                    char.map[col][row]["layer"] = "door"
                    char.map[col][row]["door"] = {**door["data"]}
                except:
                    try:
                        map["chests"][col, row]
                        char.map[col][row]["layer"] = "chest"
                    except:
                        try:
                            trap = map["traps"][col, row]
                            if trap["kind"] in ["mimic", "gas"]:
                                char.map[col][row]["layer"] = "chest"
                            elif trap["kind"] == "lever":
                                char.map[col][row]["layer"] = "lever"
                        except:
                            try:
                                mob = map["mobs"][col, row]
                                char.map[col][row]["layer"] = "mob"
                                char.map[col][row]["mob"] = mob["id_mob"]
                            except:
                                False

    return char


def updateMap(x: str, y: int, char: class_char):
    cols = list(map["base"].keys())
    try:
        ix = cols.index(x)
    except:
        raise HTTPException(status_code=404, detail="no col")

    doors = map["doors"].keys()

    ilum = 1
    try:
        ilum += char.effects["iluminate"]
    except:
        False

    for add_x in range(-ilum, ilum + 1):
        add_ix = ix + add_x
        if add_ix >= 0:
            try:
                new_x = cols[add_ix]
            except:
                new_x = False

            if new_x:
                for add_y in range(-ilum, ilum + 1):
                    new_y = y + add_y
                    try:
                        char.map[new_x][new_y]
                        if char.map[new_x][new_y]["interacted"] != "end":
                            if char.map[new_x][new_y]["layer"] == "mob":
                                if add_x in range(-1, 2) and add_y in range(-1, 2):
                                    char.mob["loc"] = [new_x, new_y]
                    except:
                        if new_y >= 1 and new_y <= 21:
                            see = True

                            kind = False
                            kind0 = False
                            kindA = False

                            test_ix = False
                            if add_x in [-2, 2]:
                                test_ix = ix + (add_x // 2)
                            test_y = False
                            if add_y in [-2, 2]:
                                test_y = y + (add_y // 2)

                            test_x = cols[test_ix]

                            if add_x in [-2, 2] and add_y == 0:
                                if (test_x, new_y) in doors:
                                    kind = "door"
                                else:
                                    kind = map["base"][test_x][new_y]
                            elif add_x == 0 and add_y in [-2, 2]:
                                if (x, test_y) in doors:
                                    kind = "door"
                                else:
                                    kind = map["base"][x][test_y]
                            elif add_x in [-2, 2] and add_y in [-1, 1]:
                                if (test_x, new_y) in doors:
                                    kind = "door"
                                else:
                                    kind = map["base"][test_x][new_y]

                                if (test_x, y) in doors:
                                    kind0 = "door"
                                else:
                                    kind0 = map["base"][test_x][y]
                            elif add_x in [-1, 1] and add_y in [-2, 2]:
                                if (new_x, test_y) in doors:
                                    kind = "door"
                                else:
                                    kind = map["base"][new_x][test_y]

                                if (x, test_y) in doors:
                                    kind0 = "door"
                                else:
                                    kind0 = map["base"][x][test_y]
                            elif add_x in [-2, 2] and add_y in [-2, 2]:
                                if (test_x, test_y) in doors:
                                    kind = "door"
                                else:
                                    kind = map["base"][test_x][test_y]

                                if (new_x, test_y) in doors:
                                    kindA = "door"
                                else:
                                    kindA = map["base"][new_x][test_y]
                                if (test_x, y) in doors:
                                    kindA0 = "door"
                                else:
                                    kindA0 = map["base"][test_x][y]

                                if (test_x, new_y) in doors:
                                    kindB = "door"
                                else:
                                    kindB = map["base"][test_x][new_y]
                                if (x, test_y) in doors:
                                    kindB0 = "door"
                                else:
                                    kindB0 = map["base"][x][test_y]

                            if kind in ["wall", "door"]:
                                see = False
                            elif kind and kind0 in ["wall", "door"]:
                                see = False
                            elif kindA:
                                if (kindA and kindA0) in ["wall", "door"]:
                                    see = False
                                elif (kindB and kindB0) in ["wall", "door"]:
                                    see = False

                            if see:
                                try:
                                    char.map[new_x]
                                except:
                                    char.map[new_x] = {}

                                try:
                                    char.map[new_x][new_y]
                                except:
                                    char.map[new_x][new_y] = {}

                                kind = map["base"][new_x][new_y]
                                char.map[new_x][new_y]["kind"] = kind

                                if kind == "empty":
                                    try:
                                        door = map["doors"][new_x, new_y]
                                        char.map[new_x][new_y]["layer"] = "door"
                                        char.map[new_x][new_y]["door"] = {
                                            **door["data"]
                                        }
                                    except:
                                        try:
                                            map["chests"][new_x, new_y]
                                            char.map[new_x][new_y]["layer"] = "chest"
                                        except:
                                            try:
                                                trap = map["traps"][new_x, new_y]
                                                if trap["kind"] in ["mimic", "gas"]:
                                                    char.map[new_x][new_y][
                                                        "layer"
                                                    ] = "chest"
                                                elif trap["kind"] == "lever":
                                                    char.map[new_x][new_y][
                                                        "layer"
                                                    ] = "lever"
                                            except:
                                                try:
                                                    mob = map["mobs"][new_x, new_y]
                                                    char.map[new_x][new_y][
                                                        "layer"
                                                    ] = "mob"
                                                    char.map[new_x][new_y]["mob"] = mob[
                                                        "id_mob"
                                                    ]
                                                    if add_x in range(
                                                        -1, 2
                                                    ) and add_y in range(-1, 2):
                                                        char.mob["loc"] = [
                                                            new_x,
                                                            new_y,
                                                        ]
                                                except:
                                                    False

    return char


def checkInteraction(x: str, y: int, block: str, char: class_char):
    try:
        xy_mob = char.mob["loc"]
        block = "mob"
        x = xy_mob[0]
        y = xy_mob[1]
    except:
        False

    try:
        interacted = char.map[x][y]["interacted"]
    except:
        interacted = False

    if interacted != "end":
        try:
            interactions = map[block + "s"][x, y]["interactions"]
        except:
            try:
                interactions = map["traps"][x, y]["interactions"]
            except:
                interactions = False

        if interactions:
            if interacted == False:
                char.map[x][y]["interacted"] = 1
                interacted = 1

            r = interactions[interacted]
            return [r, char]

    return False


def nextInteracted(x: str, y: int, char: class_char):
    if [x, y] == ["u", 4]:
        char.map[x][y]["interacted"] = 3
    else:
        char.map[x][y]["interacted"] = char.map[x][y]["interacted"] + 1
    return [False, char]


def updateInventory(items: dict, char: Union[class_char, int] = None):
    if not char:
        raise HTTPException(status_code=404, detail="no char")

    if isinstance(char, int):
        char = searchCharById(char)

    adquired = []
    for k in items.keys():
        item = searchItemById(k)

        if k in char.inventory:
            char.inventory[k].quantity += items[k]
        else:
            item.quantity = items[k]
            char.inventory[k] = item

        if char.inventory[k].quantity <= 0:
            del char.inventory[k]

        if item.kind in ["misc", "armadura", "arma"]:
            if item.effect:
                effect = item.effect
                val = effect[1] * items[k]
                try:
                    char.effects[effect[0]] += val
                except:
                    char.effects[effect[0]] = val

                if char.effects[effect[0]] <= 0:
                    del char.effects[effect[0]]

                if effect[0] in char.stats.keys():
                    char.stats[effect[0]] += val

        adquired.append(item.name)

    r = ["Has adquirido: " + ", ".join(adquired)]

    return [r, char]


def openChest(x: str, y: int, char: class_char):
    try:
        content = map["chests"][x, y]["content"]
    except:
        raise HTTPException(status_code=404, detail="no content")

    char.map[x][y]["interacted"] = "end"

    back = updateInventory(content, char)

    if [x, y] == ["t", 6]:
        if char.map["r"][9]["kind"] == "wall":
            char.map["r"][9]["kind"] = "empty"
            char.map["r"][9]["interacted"] = "end"
            back[0].append("Sientes un temblor, algo paso...")

    return back


def openDoor(x: str, y: int, char: class_char):
    try:
        door = map["doors"][x, y]["data"]
    except:
        raise HTTPException(status_code=404, detail="no door")

    open_door = False
    r = False
    if door["kind"] == "unlock":
        open_door = True
    elif door["kind"] == "lock":
        try:
            char_keys = char.inventory[7].quantity
        except:
            char_keys = 0

        if char_keys > 0:
            open_door = True
            char = updateInventory({7: -1}, char)[1]

    elif door["kind"] == "end":
        try:
            char_keys = char.inventory[8].quantity
        except:
            char_keys = 0

        if char_keys > 0:
            open_door = True
            char = updateInventory({8: -1}, char)[1]
    else:
        raise HTTPException(status_code=404, detail="unknow door kind")

    interacted = char.map[x][y]["interacted"]
    if open_door:
        char.map[x][y]["door"]["status"] = 1
        char.map[x][y]["door"]["show_inside"] = True

        if [x, y] == ["c", 4]:
            char.map[x][y]["interacted"] = 1
        elif [x, y] == ["u", 4]:
            char.map[x][y]["interacted"] = 3
        else:
            char.map[x][y]["interacted"] = "end"

        try:
            r = map["doors"][x, y]["open"][interacted]
        except:
            False
    else:
        try:
            r = map["doors"][x, y]["close"][interacted]

            try:
                map["doors"][x, y]["close"][interacted + 1]
                char.map[x][y]["interacted"] = interacted + 1
            except:
                False
        except:
            r_default = {
                1: ["La puerta esta cerrada, necesitas una llave"],
                2: ["No tienes ninguna llave, revisa tu inventario"],
            }

            if [x, y] == ["t", 3]:
                if interacted == 3:
                    interacted = 1

            r = r_default[interacted]

            if interacted == 1:
                interacted = 2
                try:
                    char.map[x][y]["interacted"] = 2
                except:
                    False

    return [r, char]


def activateTrap(x: str, y: int, char: class_char):
    try:
        trap = map["traps"][x, y]["kind"]
    except:
        raise HTTPException(status_code=404, detail="no trap")

    r = []
    hp = False
    if trap == "arrow":
        hp = 1
        r = ["Una flecha sale de la pared y te golpea"]
    elif trap == "gas":
        hp = 1
        r = ["El cofre expulsa un gas venenoso"]
    elif trap == "mimic":
        hp = 2
        r = ["El cofre era un Mimic! Te mordio :/"]
    elif trap == "lever":
        hp = 2
        r = ["Un bloque cae del techo y te golpea"]
        char.loc = [x, y]
    elif trap == "floor":
        hp = 1
        r = ["Unos pinchos se levantan del piso y te golpean"]
    elif trap == "close":
        char.map[x][y]["interacted"] = "end"

        if [x, y] == ["p", 6]:
            x_new = "p"
            y_new = 5
        elif [x, y] == ["r", 9]:
            x_new = "r"
            y_new = 10

        try:
            char = updateMap(x_new, y_new, char)
            char.loc = [x_new, y_new]
        except:
            raise HTTPException(status_code=400)

        char.map[x][y]["kind"] = "wall"

    if hp:
        char.stats["hp"] -= hp
        r.append("Perdiste " + str(hp) + " de vida")
        char.map[x][y].update({"layer": "trap", "trap": trap, "interacted": "end"})

    return [r, char]


def fightWith(x: str, y: int, char: class_char):
    try:
        mob_id = map["mobs"][x, y]["id_mob"]
    except:
        raise HTTPException(status_code=404, detail="no mob")

    mob = searchMobById(mob_id)

    char.mob["data"] = mob

    if [x, y] == ["t", 2]:
        char.map["t"][3]["interacted"] = 3

    return [False, char]


def leaveFrom(x: str, y: int, char: class_char):
    r = False

    if [x, y] == ["d", 4]:
        r = [
            "Cierras la puerta para encerrar al goblin, pero antes de lograr cerrarla te lanzo caca >.<",
            "Perdiste 1 de vida",
        ]
        char.stats["hp"] -= 1
        char.effects["olor"] = 1
        char.loc = ["b", 4]

        try:
            torch = char.inventory[9].quantity > 0
        except:
            torch = False

        if torch:
            r.append("Trabas la puerta con la antorcha para que no salga")
            char = updateInventory({9: -1}, char)[1]
            char.mob = {}
            char.map["d"][4]["interacted"] = 2
            char.map["c"][4]["interacted"] = 3
            char.map["c"][4]["door"].update({"status": 0})
        else:
            r.append(
                {
                    "msg": "No tienes con que trabar la puerta, vas a tener que pelear...",
                    "options": ["fight"],
                }
            )
    elif [x, y] == ["f", 9]:
        r = [
            {
                "msg": "El ogro ya te vio, no puede huir...",
                "options": ["fight"],
            }
        ]
    elif [x, y] == ["j", 15]:
        r = [
            {
                "msg": "El ogro ya te vio, no puede huir...",
                "options": ["fight"],
            }
        ]
        try:
            if char.map["f"][9]["interacted"] == "end":
                r = [
                    {
                        "msg": "No aprendiste con el primero? No se huye de los ogros",
                        "options": ["fight"],
                    }
                ]
        except:
            False
    elif [x, y] == ["l", 4]:
        try:
            torch = char.inventory[9].quantity > 0
        except:
            torch = False

        if torch:
            r = [
                {
                    "msg": "Ya lo despertaste con la luz de la antorcha, no puedes huir...",
                    "options": ["fight"],
                }
            ]
        else:
            try:
                interacted = char.map["l"][4]["interacted"]
            except:
                False

            if interacted == 2:
                r = ["Vuelves a caminar despacio para no despertalo"]
            else:
                r = ["Empiezas a caminar despacio para no despertalo"]
                char.map["l"][4]["interacted"] = 2

            char.mob = {}
    elif [x, y] == ["n", 9]:
        r = [
            {
                "msg": "No puedes huir de los ogros...",
                "options": ["fight"],
            }
        ]
    elif [x, y] == ["p", 16]:
        try:
            key = char.inventory[7].quantity > 0
        except:
            key = False

        if key:
            char.loc = ["n", 16]
            char.map["o"][16]["door"].update({"status": 0, "kind": "lock"})
            char.map["o"][16]["interacted"] = 3
            char.mob = {}
            r = ["Cierras la puerta con llave para que no salga"]
        else:
            r = [
                {
                    "msg": "Intentas cerrar la puerta pero el guardia te persigue, vas a tener que pelear...",
                    "options": ["fight"],
                }
            ]
    elif [x, y] == ["t", 2]:
        r = [
            "El guardia huele tu miedo y eso lo exita",
            "Cuando te das la vuelta para correr te pega un garrotazo mortal",
        ]
        char.stats["hp"] = 0
    elif [x, y] == ["t", 16]:
        char.mob = {}
        interacted = char.map["t"][16]["interacted"]

        if interacted == 1:
            r = [
                "Parece no preocuparle tu presencia y decide no seguirte",
                "Pudiste huir sin problemas",
            ]
            char.map["t"][16]["interacted"] = 2
        else:
            r = ["Sigues sin importarle"]

        try:
            if char.map["n"][4]["interacted"] == "end":
                char.map["t"][16]["interacted"] = 3
        except:
            False

        char.loc = ["s", 18]

    return [r, char]


def specialEvent(x: str, y: int, char: class_char):
    back = [False, char]

    if [x, y] == ["b", 1]:
        char.map["b"][1]["interacted"] = "end"
        back = updateInventory({9: 1}, char)
    elif [x, y] == ["b", 9]:
        char.loc = ["b", 9]
    elif [x, y] == ["c", 4]:
        char = updateInventory({9: 1}, char)[1]
        char.map["c"][4]["interacted"] = "end"
        char.mob["loc"] = ["d", 4]
        back = openDoor(x, y, char)
    elif [x, y] == ["d", 4]:
        char.map["d"][4]["interacted"] = "end"
        del char.map["d"][4]["layer"]
        del char.map["d"][4]["mob"]
    elif [x, y] == ["o", 16]:
        open = openDoor(x, y, char)
        if open[0] == False:
            char = open[1]
            char.mob["loc"] = ["p", 16]
            back = fightWith("p", 16, char)
        else:
            back = open
    elif [x, y] == ["p", 6]:
        char.map[x][y]["kind"] = "wall"
        char.loc = ["o", 6]
    elif [x, y] == ["r", 9]:
        char.map[x][y]["kind"] = "wall"
        char.loc = ["r", 8]
    elif [x, y] == ["t", 16]:
        try:
            char.inventory[14]
            back[0] = [
                "El goblin toma la mascara, grita algo sobre los 'zurdos' y se va"
            ]
            del char.map["t"][16]["layer"]
            del char.map["t"][16]["mob"]
            char.map["t"][16]["interacted"] = "end"
        except:
            back[0] = [
                "Que paso? No tienes la mascara en el inventario",
                {"msg": "Que vas a hacer", "options": ["fight", "leave"]},
            ]
    elif [x, y] == ["u", 4]:
        back[0] = "restart"

    return back


async def selectClass(clase: str, id_char: int):
    add_items = False

    if clase == "mage":
        add_items = {4: 1, 6: 1}
    elif clase == "warrior":
        add_items = {3: 1, 5: 1}
    elif clase == "tank":
        add_items = {11: 1, 12: 1}

    if add_items:
        add = updateInventory(add_items, id_char)
        await updateChar(add[1])
        return add[0]
    else:
        raise HTTPException(status_code=404, detail="error clase")


# methods ------------------------------------------------------------------------------------
@router.get("/", status_code=200)
async def index():
    return "chars"


@router.get("/getElementById/{id}", response_model={}, status_code=200)
async def getElementById(id: int):
    if not id:
        raise HTTPException(status_code=400, detail="Error de formulario")

    return {"value": searchCharById(id)}


@router.post("/getElement", response_model=[], status_code=200)
async def getElement(filters: dict):
    if not filters:
        raise HTTPException(status_code=400, detail="Error de formulario")

    return {"value": searchChar(filters)}


@router.post("/add", status_code=201)
async def add(data: Annotated[str, Form()] = None):
    if not data:
        raise HTTPException(status_code=400, detail="Error de formulario")

    try:
        last_char_id = list_class_default[-1].id
    except:
        last_char_id = 3

    if last_char_id < 3:
        last_char_id = 3

    new_id = last_char_id + 1

    data_dict = loads(data)
    data_dict["id"] = new_id

    list_class_default.append(data_dict)
    list_class.append(class_char(**data_dict))

    await selectClass(data_dict["clase"], new_id)

    return {"value": new_id}


@router.delete("/{id}", status_code=204)
async def delete(id: int):
    if not id:
        raise HTTPException(status_code=400, detail="Error de formulario")

    if id in [1, 2]:
        await restart(id)
    else:
        found = False

        for i, x in enumerate(list_class_default):
            if x["id"] == id:
                found = True
                break

        if not found:
            raise HTTPException(
                status_code=404, detail="No existe informacion del personaje"
            )

        found = False
        for k, y in enumerate(list_class):
            if y.id == id:
                found = True
                break

        if not found:
            raise HTTPException(status_code=404, detail="Personaje no encontrada")

        if found:
            del list_class_default[i]
            del list_class[k]


@router.post("/update")
async def update(char: Annotated[str, Form()] = None):
    if not char:
        raise HTTPException(status_code=400, detail="Error de formulario")

    found = False

    char_dict = loads(char)
    char = class_char(**char_dict)

    map = {}
    for x, vx in char.map.items():
        map[x] = {}
        for y, vy in vx.items():
            map[x][int(y)] = vy
    char.map = map

    for i, x in enumerate(list_class):
        if x.id == char.id:
            list_class[i] = char
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="No se encontro al personaje")


@router.get("/restart/{id}", status_code=204)
async def restart(id: int):
    if not id:
        raise HTTPException(status_code=400, detail="Error de formulario")

    found = False

    char_def = searchCharDefaultById(id)

    for k, y in enumerate(list_class):
        if y.id == id:
            list_class[k] = class_char(**char_def)
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="No se encontro al personaje")


@router.get("/checkMove")
async def checkMove(x: str, y: int, id: int):
    if not (x or y or id):
        raise HTTPException(status_code=400, detail="Error de formulario")

    char = searchCharById(id)

    block = char.map[x][y]["kind"]
    if block == "empty":
        try:
            block = char.map[x][y]["layer"]
        except:
            False
    if block == "door":
        if char.map[x][y]["door"]["status"] == 1:
            block = "empty"
    if block == "mob":
        char.mob["loc"] = [x, y]

    if id == 1:
        default = {
            "a": {1: {"kind": "wall"}},
            "b": {1: {"kind": "empty"}},
            "c": {1: {"kind": "wall"}},
        }
        if char.map == default:
            char = updateMapAll(char)
        if block in ["empty", "wall", "trap"]:
            char.loc = [x, y]
    else:
        if block in ["empty", "trap"]:
            char.loc = [x, y]
            char = updateMap(x, y, char)

    if block != "wall":
        check = checkInteraction(x, y, block, char)

        if check:
            r = check[0]
            char = check[1]

    await updateChar(char)

    try:
        return {"value": r}
    except:
        raise HTTPException(status_code=204)


@router.get("/handleOption")
async def handleOption(x: str, y: int, op: str, id: int):
    if not (x or y or op or id):
        raise HTTPException(status_code=400, detail="Error de formulario")

    char = searchCharById(id)

    try:
        xy_mob = char.mob["loc"]
        x = xy_mob[0]
        y = xy_mob[1]
    except:
        False

    interacted = char.map[x][y]["interacted"]

    block = char.map[x][y]["kind"]
    if block == "empty":
        try:
            map["traps"][x, y]["kind"]
            block = "trap"
        except:
            try:
                block = char.map[x][y]["layer"]
            except:
                False

    if block == "chest":
        op_list = {"y": "openChest", "n": False}
    else:
        try:
            op_list = map[block + "s"][x, y]["events"][interacted]
        except:
            try:
                op_list = map["traps"][x, y]["events"][interacted]
            except:
                raise HTTPException(status_code=204)

    try:
        event = op_list[op]
    except:
        raise HTTPException(status_code=404, detail="unknown op")

    if event:
        functions = {
            "nextInteracted": nextInteracted,
            "openChest": openChest,
            "openDoor": openDoor,
            "activateTrap": activateTrap,
            "specialEvent": specialEvent,
            "leaveFrom": leaveFrom,
            "fightWith": fightWith,
        }

        try:
            handleEvent = functions[event]
        except:
            raise HTTPException(status_code=405, detail="unknown event")

        event_return = handleEvent(x, y, char)

        r = event_return[0]
        new = event_return[1]

        if new:
            await updateChar(new)

        return {"value": r}
    else:
        raise HTTPException(status_code=204)


@router.post("/handleFight")
async def handleFight(turn: Annotated[str, Form()], id: Annotated[int, Form()]):
    if not (turn or id):
        raise HTTPException(status_code=400, detail="Error de formulario")

    char = searchCharById(id)
    turn = loads(turn)

    if turn["current"] == "char":
        if turn["state"] == "results":
            if turn["char"] == "attack":
                mob_stats = char.mob["data"].stats

                damage = char.stats["damage"]
                defence = mob_stats["defence"]
                hp = mob_stats["hp"]
                hit = damage - defence
                new_hp = hp - hit
                if new_hp < 0:
                    new_hp = 0

                mob_stats["hp"] = new_hp
                mob_stats["defence"] -= 1
                if mob_stats["defence"] < 0:
                    mob_stats["defence"] = 0

                turn["msg"] = "Golpeaste al mob, le hiciste " + str(hit) + " de daño"

    elif turn["current"] == "mob":
        if turn["state"] == "results":
            if turn["mob"] == "attack":
                damage = char.mob["data"].stats["damage"]
                defence = char.stats["defence"]
                hp = char.stats["hp"]
                hit = damage - defence
                new_hp = hp - hit
                if new_hp < 0:
                    new_hp = 0

                char.stats["hp"] = new_hp
                if turn["char"] != "defence":
                    char.stats["defence"] -= 1
                    if char.stats["defence"] < 0:
                        char.stats["defence"] = 0

                turn["msg"] = "El mob te golpea, te hizo " + str(hit) + " de daño"

    await updateChar(char)
    return {"value": turn}


@router.get("/endFight/{id}")
async def endFight(id: int):
    if not id:
        raise HTTPException(status_code=400, detail="Error de formulario")

    char = searchCharById(id)
    r = False

    char_def = searchCharDefaultById(id)
    char.stats["defence"] = char_def["stats"]["defence"]

    if char.mob["data"].stats["hp"] <= 0:
        char.xp += char.mob["data"].xp

        x = char.mob["loc"][0]
        y = char.mob["loc"][1]
        del char.map[x][y]["layer"]
        del char.map[x][y]["mob"]
        char.map[x][y]["interacted"] = "end"

        if char.xp >= list(levels[char.level])[-1]:
            new_level = False
            for lvl, rg in levels.items():
                if lvl > char.level:
                    if char.xp in rg:
                        new_level = lvl
                        break
            if new_level:
                stats_points = new_level - char.level
                if stats_points <= 0:
                    raise HTTPException(status_code=404, detail="error level dif")
                else:
                    char.level = new_level
                    r = stats_points

    char.mob = {}
    await updateChar(char)

    if r:
        return {"value": r}
    else:
        raise HTTPException(status_code=204)


@router.get("/useConsumable")
async def useConsumable(id_item: int, id_char: int):
    if not (id_item or id_char):
        raise HTTPException(status_code=400, detail="Error de formulario")

    char = searchCharById(id_char)

    r = False

    try:
        item = char.inventory[id_item]
    except:
        raise HTTPException(
            status_code=404, detail="El objeto no esta en el inventario"
        )

    if item.kind != "consumible":
        r = ["Objeto no consumible"]

    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Objeto sin existencias")

    used = False
    effect = item.effect
    if effect[0] == "hp":
        if char.stats["hp"] >= char.stats["hp_max"]:
            r = ["Vida ya al maximo"]
        else:
            char.stats["hp"] += effect[1]
            if char.stats["hp"] > char.stats["hp_max"]:
                char.stats["hp"] = char.stats["hp_max"]

            if effect[1] >= 0:
                r = ["Recuperaste " + str(effect[1]) + " de vida"]
            else:
                r = [
                    "Perdiste " + str(effect[1]) + " de vida",
                    "Eso de comer caca no es un fetiche, verdad?...",
                ]

            used = True
    elif effect[0] == "olor":
        try:
            r = ["Ya era hora de que limpiaras"]
            char.effects["olor"] += effect[1]
            if char.effects["olor"] <= 0:
                del char.effects["olor"]
            used = True
        except:
            r = ["No lo necesitas"]
    else:
        r = ["No hizo efecto"]

    if used:
        char = updateInventory({item.id: -1}, char)[1]

    await updateChar(char)

    return {"value": r}


# methods admin ------------------------------------------------------------------------------------
@router.get("/getAllItems")
async def getAllItems():
    char = searchCharById(1)

    for item in list_items:
        add = copy.deepcopy(item)
        add.quantity = 1
        char.inventory[item.id] = add
    await updateChar(char)

    return ["Obtuviste todos los items"]
