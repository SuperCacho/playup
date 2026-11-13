#  Play Up — Sistema de Gestión de Videojuegos

**Play Up** es un proyecto integrador desarrollado para la materia **Programación II**. Consiste en una aplicación web diseñada para reemplazar una planilla de Excel utilizada para registrar, organizar y consultar una colección personal de videojuegos.

La plataforma permite a cada usuario administrar su propia biblioteca de forma privada, consultar estadísticas de actividad y progresar en un sistema de rangos basado en sus horas de juego y cantidad de títulos registrados.

---

##  Características principales

- ** Autenticación segura:** Registro e inicio de sesión con cuentas individuales. Los datos de cada usuario permanecen aislados.
- ** Gestión de videojuegos (CRUD):** Permite agregar, visualizar, editar y eliminar videojuegos de la biblioteca.
- ** Baja lógica:** Los juegos eliminados permanecen almacenados en la base de datos, pero dejan de mostrarse en la biblioteca.
- ** Búsqueda de portadas:** Integración con la base de datos de Steam para obtener automáticamente las imágenes de los videojuegos.
- ** Dashboard estadístico:** Gráficos interactivos con información sobre la colección, estados de los juegos, actividad reciente y géneros más jugados.
- ** Perfil personalizado:** Posibilidad de configurar una imagen de perfil y consultar el progreso personal.
- ** Sistema de rangos:** Clasificación de usuarios desde *Novato* hasta *Dios Gamer*, según las horas acumuladas y la cantidad de juegos registrados.
- ** Panel de administración:** Gestión de usuarios mediante búsqueda por correo electrónico y activación o desactivación de cuentas.
- ** Diseño responsive:** Interfaz adaptable a computadoras, tablets y celulares, con menú lateral colapsable.

---

##  Manual de usuario

### 1. Registro e inicio de sesión

Al ingresar a la aplicación, el usuario puede crear una cuenta nueva o iniciar sesión con una existente.

- Registro de nuevas cuentas.
- Inicio de sesión con credenciales.
- Opción **Mantener sesión iniciada** para recordar la cuenta en el navegador.
- Redirección automática a la pantalla principal después de autenticarse, evitando conflictos de navegación.

### 2. Biblioteca

Es la pantalla principal de la aplicación y el núcleo de la gestión de videojuegos.

Los juegos se presentan mediante tarjetas que incluyen información como portada, título, puntuación, horas jugadas y estado.

**Operaciones disponibles:**

- **Agregar:** Mediante el botón flotante inferior se abre un formulario para registrar un nuevo videojuego. El título es el único campo obligatorio.
- **Buscar portada:** El botón de búsqueda permite consultar Steam para obtener automáticamente la portada correspondiente.
- **Editar:** Permite modificar la información de un videojuego existente.
- **Eliminar:** Ejecuta una baja lógica. El juego desaparece de la biblioteca, pero permanece registrado en la base de datos.
- **Buscar:** La barra superior permite filtrar los videojuegos por nombre en tiempo real.

### 3. Dashboard estadístico

Ofrece una vista general de la actividad y el estado de la colección mediante indicadores y gráficos interactivos.

Incluye:

- Cantidad total de videojuegos registrados.
- Porcentaje de juegos completados.
- Total de horas jugadas.
- Promedio de puntuación.
- Distribución de videojuegos según su estado.
- Actividad reciente de carga de juegos.
- Géneros más jugados.

### 4. Mi perfil y ranking

**Mi perfil**

Permite personalizar la cuenta mediante una imagen de perfil, ingresando un enlace de imagen, y consultar el rango actual junto con una barra de progreso.

**Ranking**

Muestra el sistema completo de rangos, incluyendo los requisitos necesarios para alcanzar cada categoría.

La clasificación comienza en **Novato** y progresa hasta llegar a **Dios Gamer**, incentivando el registro y seguimiento de la actividad dentro de la plataforma.

### 5. Gestión de usuarios (Solo administradores)

Los usuarios con permisos de administrador disponen de una pestaña adicional para gestionar las cuentas registradas.

Funcionalidades:

- Buscar usuarios mediante su correo electrónico.
- Consultar las cuentas registradas.
- Activar o desactivar cuentas.
- Protección contra la desactivación accidental de la cuenta del administrador principal.

---

##  Arquitectura y tecnologías

El proyecto utiliza una arquitectura cliente-servidor, separando la interfaz de usuario de la lógica de negocio y el acceso a los datos.

### Frontend

| Tecnología | Uso |
|---|---|
| Vue 3 | Framework para la interfaz de usuario |
| Vite | Herramienta de desarrollo y compilación |
| Vue Router | Gestión de rutas y navegación |
| Axios | Comunicación HTTP con el backend |
| Chart.js | Visualización de estadísticas y gráficos |

### Backend

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| FastAPI | Framework para la API REST |
| Pydantic | Validación y estructuración de datos |

### Base de datos y servicios

| Tecnología | Uso |
|---|---|
| PostgreSQL | Base de datos relacional |
| Supabase | Alojamiento de base de datos y autenticación |
| Steam | Fuente externa para la búsqueda de portadas |

---

##  Seguridad e integridad de datos

El sistema implementa diferentes mecanismos para proteger la información de los usuarios y mantener la integridad de la base de datos.

- **Contraseñas:** Supabase Auth administra las credenciales y utiliza hashing mediante bcrypt. Las contraseñas no se almacenan en texto plano.
- **Autenticación mediante JWT:** El frontend administra la sesión y el backend verifica la autenticidad del token en cada petición protegida.
- **Protección de rutas:** Se validan los permisos y roles de usuario para restringir el acceso a determinadas secciones.
- **Aislamiento de información:** Cada usuario puede acceder únicamente a los videojuegos de su propia biblioteca.
- **Baja lógica:** Los registros de videojuegos se conservan mediante un campo booleano `activo`, evitando la eliminación física de información.
- **Integridad relacional:** La base de datos utiliza un modelo normalizado bajo los principios de la Tercera Forma Normal (3FN).

### Modelo de datos

El modelo relacional contempla las siguientes relaciones principales:

- **Usuarios - Videojuegos:** Relación uno a muchos (1:N).
- **Videojuegos - Géneros:** Relación muchos a muchos (N:M), implementada mediante una tabla pivote.

---

##  Objetivo del proyecto

El objetivo de Play Up es desarrollar una solución web que permita administrar colecciones personales de videojuegos de manera organizada, intuitiva y segura.

Además de resolver una necesidad concreta de gestión de información, el proyecto permite aplicar conocimientos de programación frontend y backend, desarrollo de API REST, bases de datos relacionales, autenticación, seguridad y visualización de datos.

---

##  Contexto académico

| Información | Detalle |
|---|---|
| Proyecto | Play Up |
| Tipo | Proyecto Integrador |
| Materia | Programación II |
| Tecnologías principales | Vue 3, Python, FastAPI y PostgreSQL |

---

**Play Up — Tu colección, tus estadísticas, tu progreso.** 🎮🏆
