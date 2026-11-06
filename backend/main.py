from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import juegos

app = FastAPI(title="PlayUp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(juegos.router)


@app.get("/")
def root():
    return {"status": "ok", "mensaje": "PlayUp API funcionando perfectamente"}
