import urllib.parse
import uuid

import requests
import schemas
from database import supabase
from fastapi import APIRouter, Depends, Header, HTTPException

router = APIRouter(prefix="/api/juegos", tags=["Juegos"])


def obtener_usuario_actual(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado: Falta el token")
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception as e:
        print(f" ERROR TOKEN: {e!s}")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


@router.get("/catalogos")
def obtener_catalogos():
    try:
        return {
            "estados": supabase.table("estados").select("*").execute().data,
            "generos": supabase.table("generos").select("*").execute().data,
            "categorias": supabase.table("categorias").select("*").execute().data,
            "opiniones": supabase.table("opiniones").select("*").execute().data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/buscar-imagen/{titulo}")
def buscar_imagen_steam(titulo: str):
    try:
        titulo_codificado = urllib.parse.quote(titulo)
        url = f"https://store.steampowered.com/api/storesearch/?term={titulo_codificado}&l=english&cc=US"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get("total", 0) > 0:
            app_id = data["items"][0]["id"]
            return {
                "portada_url": f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg",
                "encontrado": True,
            }
        return {"portada_url": None, "encontrado": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar imagen: {e!s}")


@router.get("/", response_model=list[schemas.JuegoResponse])
def obtener_juegos(usuario_id: str = Depends(obtener_usuario_actual)):
    try:
        response = (
            supabase.table("juegos")
            .select("*, juegos_generos(generos(*))")
            .eq("activo", True)
            .eq("usuario_id", usuario_id)
            .execute()
        )
        juegos_limpios = []
        for j in response.data:
            j["generos"] = [g["generos"] for g in j.get("juegos_generos", [])]
            del j["juegos_generos"]
            juegos_limpios.append(j)
        return juegos_limpios
    except Exception as e:
        print(f" ERROR BD: {e!s}")
        raise HTTPException(status_code=500, detail=f"Error al obtener juegos: {e!s}")


@router.post("/", response_model=schemas.JuegoResponse)
def crear_juego(
    juego: schemas.JuegoCreate, usuario_id: str = Depends(obtener_usuario_actual)
):
    datos = juego.model_dump()
    generos_ids = datos.pop("generos", [])
    datos["id"] = str(uuid.uuid4())
    datos["activo"] = True
    datos["usuario_id"] = usuario_id
    try:
        response = supabase.table("juegos").insert(datos).execute()
        nuevo_juego = response.data[0]
        if generos_ids:
            relaciones = [
                {"juego_id": datos["id"], "genero_id": gid} for gid in generos_ids
            ]
            supabase.table("juegos_generos").insert(relaciones).execute()
            nuevo_juego["generos"] = (
                supabase.table("generos")
                .select("*")
                .in_("id", generos_ids)
                .execute()
                .data
            )
        else:
            nuevo_juego["generos"] = []
        return nuevo_juego
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear: {e!s}")


@router.put("/{juego_id}", response_model=schemas.JuegoResponse)
def actualizar_juego(
    juego_id: str,
    juego_actualizado: schemas.JuegoCreate,
    usuario_id: str = Depends(obtener_usuario_actual),
):
    datos = juego_actualizado.model_dump()
    generos_ids = datos.pop("generos", [])
    try:
        response = (
            supabase.table("juegos")
            .update(datos)
            .eq("id", juego_id)
            .eq("usuario_id", usuario_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(
                status_code=404, detail="Juego no encontrado o no tenés permiso"
            )

        supabase.table("juegos_generos").delete().eq("juego_id", juego_id).execute()
        if generos_ids:
            relaciones = [
                {"juego_id": juego_id, "genero_id": gid} for gid in generos_ids
            ]
            supabase.table("juegos_generos").insert(relaciones).execute()
            response.data[0]["generos"] = (
                supabase.table("generos")
                .select("*")
                .in_("id", generos_ids)
                .execute()
                .data
            )
        else:
            response.data[0]["generos"] = []
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {e!s}")


@router.delete("/{juego_id}")
def eliminar_juego(juego_id: str, usuario_id: str = Depends(obtener_usuario_actual)):
    try:
        response = (
            supabase.table("juegos")
            .update({"activo": False})
            .eq("id", juego_id)
            .eq("usuario_id", usuario_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(
                status_code=404, detail="Juego no encontrado o no tenés permiso"
            )
        return {"mensaje": "Juego eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {e!s}")
