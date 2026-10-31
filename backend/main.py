from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(tittle="PlayUp API", description="Backend para la gestion de jeugos")

"""configuraicon de CORS(para que vue pueda conectarse despues)"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # esto tendra la url de vue, no importa el error
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def ruta_raiz():
    return {"mensaje": "El backend esta funcionando"}
