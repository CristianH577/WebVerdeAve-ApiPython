from fastapi import APIRouter, HTTPException, Request, Form


# configs ----------------------------------------------------------------------
router = APIRouter(
    prefix="/mechanics",
    tags=["mechanics"],
    responses={404: {"error": "Error de router mecanicas"}},
)


# function ----------------------------------------------------------------------------------------------
def keys_to_int(item):
    if isinstance(item, dict):
        try:
            return {int(k): keys_to_int(v) for k, v in item.items()}
        except:
            False
    return item


# urls ----------------------------------------------------------------------------------------------
@router.get("/")
async def index():
    print("mecanicas")


@router.post("/makeBase")
async def makeBase(request: Request):
    data = await request.json()

    map = {}
    for row in range(1, data["rows"] + 1):
        map[row] = {}
        for col in range(1, data["cols"] + 1):
            map[row][col] = {"kind": "empty"}

    return {"value": map}


@router.post("/showCells")
async def showCells(request: Request):
    data = await request.json()

    try:
        map_base = data["map_base"]
        test_data = data["test_data"]
        row = int(data["row"])
        col = int(data["col"])
        ilumination = int(data["ilumination"])
    except:
        raise HTTPException(status_code=404, detail="Error de formulario")

    map_base = keys_to_int(map_base)
    map = keys_to_int(test_data["map"])

    rows_len = len(map_base.keys())
    cols_len = len(map_base[1].keys())

    # marco los vistos
    for i in range(1, rows_len + 1):
        for j in range(1, cols_len + 1):
            try:
                map[i][j]["seen"]
                map[i][j]["seen"] = 4
            except:
                False

    allow_see = ["empty", "door_open", "enemy", "trap"]
    allownt_see = ["wall", "door_closed"]

    try:
        kind = map[row][col]["kind"]
    except:
        kind = map_base[row][col]["kind"]

    if kind in allownt_see:
        kind_new = kind

        # reviso si es la primera vez que veo la puerta cerrada
        try:
            map[row][col]["seen"]
            if kind == "door_closed":
                kind_new = "door_open"
        except:
            False

        map[row][col]["kind"] = kind_new
        map[row][col]["seen"] = 1

        current = test_data["current"]
    else:
        current = [row, col]

        cuandrantes = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        for cuandrante in cuandrantes:
            for i in range(0, ilumination + 1):
                for j in range(0, ilumination + 1):
                    x = row + i * cuandrante[0]
                    y = col + j * cuandrante[1]

                    if 0 < x <= rows_len and 0 < y <= cols_len:
                        # reviso si vi la celda
                        try:
                            seen = map[x][y]["seen"]
                        except:
                            seen = 0

                        # reviso si se vera la celda
                        if not seen:
                            # las celda seleccionada
                            if x == row and y == col:
                                seen = 1
                            else:
                                r = x - (1 * cuandrante[0])
                                c = y - (1 * cuandrante[1])

                                # las celdas en la misma fila
                                if x == row:
                                    try:
                                        if map[x][c]["seen"]:
                                            if map[x][c]["kind"] in allow_see:
                                                seen = 2
                                    except:
                                        False

                                # las celdas en la misma columna
                                elif y == col:
                                    try:
                                        if map[r][y]["seen"]:
                                            if map[r][y]["kind"] in allow_see:
                                                seen = 2
                                    except:
                                        False

                                # reviso la diagonal
                                else:
                                    try:
                                        if map[r][c]["seen"]:
                                            if map[r][c]["kind"] in allow_see:
                                                # reviso la contradiagonal
                                                try:
                                                    if map[r][y]["seen"]:
                                                        if (
                                                            map[r][y]["kind"]
                                                            in allow_see
                                                        ):
                                                            seen = 3
                                                except:
                                                    False
                                                try:
                                                    if map[x][c]["seen"]:
                                                        if (
                                                            map[x][c]["kind"]
                                                            in allow_see
                                                        ):
                                                            seen = 3
                                                except:
                                                    False
                                    except:
                                        False

                        if seen:
                            if seen == 4:
                                # remarco seen
                                if x == row and y == col:
                                    seen = 1
                                else:
                                    if x == row or y == col:
                                        seen = 2
                                    else:
                                        seen = 3
                            map[x][y]["seen"] = seen

                            # reviso el tipo de celda
                            if x == row and y == col:
                                kind_new = map_base[x][y]["kind"]
                                # reviso si hay una trampa y la activo
                                if kind_new != "trap":
                                    try:
                                        kind_new = map[x][y]["kind"]
                                    except:
                                        False
                            else:
                                try:
                                    map[x][y]["kind"]
                                    kind_new = False
                                except:
                                    kind_new = map_base[x][y]["kind"]

                                    # reviso si hay una trampa y la oculto
                                    if kind_new == "trap":
                                        kind_new = "empty"

                            if kind_new:
                                map[x][y]["kind"] = kind_new

    response = {"map": map, "current": current}
    return {"value": response}
