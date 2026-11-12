from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, juegos

app = FastAPI(title="PlayUp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(juegos.router)
app.include_router(auth.router)


@app.get("/")
def ruta_raiz():
    return {"mensaje": "El backend de PlayUp está funcionando"}
