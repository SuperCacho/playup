#  Play Up

**Play Up** es una aplicación web desarrollada como Proyecto Integrador para la materia Programación II. Surge de la necesidad de reemplazar una planilla de Excel utilizada para registrar, organizar y consultar una colección personal de videojuegos.

##  Tecnologías Utilizadas

*   **Frontend:** Vue 3 (Composition API), Vite, Axios, Font Awesome.
*   **Backend:** Python 3, FastAPI, Uvicorn, Pydantic.
*   **Base de Datos:** PostgreSQL (alojado en Supabase).
*   **Control de Versiones:** Git y GitHub.

##  Arquitectura

El proyecto sigue una arquitectura de 3 capas:
1.  **Frontend (Vue):** Interfaz de usuario. Se comunica con el backend mediante peticiones HTTP (API REST).
2.  **Backend (FastAPI):** Lógica de negocio y validación de datos (Pydantic). Se conecta a la base de datos usando el SDK oficial de Supabase para Python.
3.  **Base de Datos (Supabase):** Almacena la información de manera relacional. Incluye una tabla principal (`juegos`) y tablas satélite (`estados`, `categorias`, `opiniones`, `generos`).

*Nota:* Se implementó **baja lógica** para la eliminación de registros (el campo `activo` pasa a `False` en lugar de borrar la fila físicamente).

## 🛠️ Instalación y Ejecución (Para Desarrolladores)

### Requisitos previos
*   Python 3.10 o superior.
*   Node.js (para el frontend).
*   Una cuenta en Supabase y un proyecto creado.

### 1. Clonar el repositorio
```bash
git clone https://github.com/SuperCacho/playup.git
cd playup