from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routers import chars, analyze


#  -----------------------------------------------------------------------------------------
app = FastAPI()
# uvicorn main:app --reload

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chars.router)
app.include_router(analyze.router)


# methods --------------------------------------------------------------------------------
@app.get("/")
async def index():
    return "ON"


@app.get("/error")
async def error():
    raise HTTPException(status_code=404, detail="error de testeo")
