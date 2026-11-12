#  Play Up (v2.0)

**Play Up** es una aplicación web integral desarrollada como Proyecto Integrador para la materia Programación II. Reemplaza el uso de planillas de cálculo para gestionar una biblioteca personal de videojuegos.

##  Tecnologías Utilizadas
*   **Frontend:** Vue 3 (Composition API), Vue Router, Vite, Axios, Font Awesome.
*   **Backend:** Python 3, FastAPI, Uvicorn, Pydantic, Supabase SDK.
*   **Base de Datos:** PostgreSQL (Supabase).

##  Características Principales (Nuevas)
*   **Autenticación:** Sistema de Login y Registro conectado a Supabase Auth.
*   **Enrutamiento (SPA):** Navegación fluida entre Dashboard, Biblioteca y Perfil sin recargar la página (Vue Router).
*   **Relaciones N:M:** Los juegos se vinculan con múltiples géneros a través de una tabla pivote (`juegos_generos`).
*   **Dashboard Estadístico:** Gráficos dinámicos de distribución por Estado y Top Géneros, calculados en tiempo real.
*   **Perfil Gamer:** Rangos dinámicos (Novato, Veterano, Élite) calculados según la cantidad de juegos y horas jugadas. Permite personalizar el avatar.
*   **Formularios Dinámicos:** Los estados y géneros se cargan desde la base de datos real (no están hardcodeados).

##  Instalación y Ejecución

### 1. Backend (Python)
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
# Crear archivo .env con SUPABASE_URL y SUPABASE_KEY
uvicorn main:app --reload