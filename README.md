# Play Up - Sistema de Gestión de Videojuegos

Play Up es un proyecto integrador desarrollado para la materia Programación II. La aplicación web surge para resolver la necesidad de reemplazar una planilla de Excel utilizada para registrar y organizar una colección personal de videojuegos.

El sistema permite llevar un control detallado y visual de los juegos, evitando la pérdida de información, facilitando la búsqueda y ofreciendo estadísticas en tiempo real sobre la colección.

## Funcionalidades Principales

*   **Gestión de usuarios:** Registro e inicio de sesión seguro utilizando tokens JWT. Los datos de cada usuario están completamente aislados; cada persona ve únicamente su propia biblioteca.
*   **CRUD Completo:** Permite agregar, leer, editar y eliminar videojuegos. La eliminación se realiza de forma lógica (el juego se marca como inactivo en la base de datos, no se borra físicamente).
*   **Integración con API externa:** Búsqueda y carga automática de portadas de videojuegos en alta calidad conectándose con la base de datos de la tienda Steam.
*   **Panel de Administrador:** Un perfil con permisos especiales que permite buscar usuarios por correo electrónico y desactivar o reactivar sus cuentas.
*   **Dashboard estadístico:** Visualización de datos mediante gráficos interactivos, incluyendo distribución por estado, actividad reciente y géneros más jugados.
*   **Sistema de Rangos:** Los usuarios escalan de nivel (desde Novato hasta Dios Gamer) basándose en las horas totales jugadas y la cantidad de juegos registrados.

## Tecnologías Utilizadas

*   **Frontend:** Vue 3 (Composition API), Vite, Vue Router, Axios, Chart.js.
*   **Backend:** Python 3, FastAPI, Uvicorn, Pydantic.
*   **Base de Datos:** PostgreSQL alojado en Supabase. El modelo está normalizado e incluye relaciones de uno a muchos (1:N) y muchos a muchos (N:M) mediante tablas pivote.

## Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/SuperCacho/playup.git
cd playup
