import uuid

import schemas
from database import supabase
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/juegos", tags=["Juegos"])


@router.get("/", response_model=list[schemas.JuegoResponse])
def obtener_juegos():
    try:
        response = supabase.table("juegos").select("*").eq("activo", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener: {e!s}")


@router.post("/", response_model=schemas.JuegoResponse)
def crear_juego(juego: schemas.JuegoCreate):
    datos = juego.model_dump()
    datos["id"] = str(uuid.uuid4())
    datos["activo"] = True

    try:
        response = supabase.table("juegos").insert(datos).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear: {e!s}")


@router.delete("/{juego_id}")
def eliminar_juego(juego_id: str):
    try:
        # Baja logica: en vez de delete, hacemos un udapte de activo a false
        response = (
            supabase.table("juegos")
            .update({"activo: False"})
            .eq("id", juego_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Juego no encontrado")

        return {"mensaje:Juego eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {e!s}")
