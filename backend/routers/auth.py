import schemas
from database import supabase
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
def registrar_usuario(user: schemas.UserRegister):
    try:
        res = supabase.auth.sign_up({"email": user.email, "password": user.password})
        username = user.email.split("@")[0]
        supabase.table("perfiles").insert(
            {
                "id": res.user.id,
                "username": username,
                "email": user.email,
                "rol": "coleccionista",
                "activo": True,
            }
        ).execute()
        return {"mensaje": "Usuario registrado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar: {e!s}")


@router.post("/login")
def login_usuario(user: schemas.UserLogin):
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        perfil = supabase.table("perfiles").select("*").eq("id", res.user.id).execute()

        if not perfil.data:
            raise HTTPException(status_code=401, detail="Perfil no encontrado")

        datos_perfil = perfil.data[0]

        if not datos_perfil.get("activo", True):
            raise HTTPException(
                status_code=403,
                detail="Tu cuenta ha sido desactivada por un administrador.",
            )

        return {"token": res.session.access_token, "rol": datos_perfil["rol"]}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@router.get("/usuarios")
def obtener_usuarios(search: str | None = Query(None)):
    try:
        query = supabase.table("perfiles").select("*")
        if search:
            query = query.or_(f"username.ilike.%{search}%,email.ilike.%{search}%")
        res = query.execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/usuarios/{user_id}/toggle")
def alternar_estado_usuario(user_id: str):
    try:
        user = (
            supabase.table("perfiles")
            .select("activo", "rol")
            .eq("id", user_id)
            .execute()
        )
        if not user.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # PROTECCIÓN DEL ADMIN: Si es admin, no se puede desactivar
        if user.data[0]["rol"] == "admin":
            raise HTTPException(
                status_code=403,
                detail="No se puede desactivar a la cuenta de Administrador principal.",
            )

        estado_actual = user.data[0].get("activo", True)
        nuevo_estado = not estado_actual

        supabase.table("perfiles").update({"activo": nuevo_estado}).eq(
            "id", user_id
        ).execute()
        accion = "activado" if nuevo_estado else "desactivado"
        return {"mensaje": f"Usuario {accion}", "activo": nuevo_estado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cambiar estado: {e!s}")
