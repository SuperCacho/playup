Play Up - Sistema de Gestión de Videojuegos
Play Up es un Proyecto Integrador desarrollado para la materia Programación II. Consiste en una aplicación web que resuelve la necesidad de reemplazar una planilla de Excel utilizada para registrar, organizar y consultar una colección personal de videojuegos.
El sistema permite a los usuarios gestionar su propia biblioteca de forma privada, visualizar estadísticas de su actividad y escalar en un sistema de rangos basado en sus horas de juego.
Características Principales
Autenticación Segura: Registro e inicio de sesión. Los datos de cada usuario están aislados; cada cuenta ve únicamente sus propios juegos.
Gestión Completa: Permite agregar, visualizar, editar y eliminar videojuegos. La eliminación es de tipo lógico (el registro permanece guardado en la base de datos pero se oculta de la vista).
Búsqueda de Portadas: Integración automática con la base de datos de la tienda Steam para cargar las imágenes de los juegos.
Dashboard Estadístico: Gráficos interactivos que muestran la distribución por estado, actividad reciente y géneros más jugados.
Panel de Administrador: Interfaz exclusiva para gestionar usuarios (búsqueda, activación y desactivación de cuentas). Las cuentas de administrador están protegidas contra auto-desactivación.
Sistema de Rangos: Clasificación de usuarios desde "Novato" hasta "Dios Gamer" según sus horas acumuladas y cantidad de juegos.
Diseño Responsive: Interfaz adaptada para computadoras, tablets y celulares con menú lateral colapsable.

Manual de Usuario
1. Registro e Inicio de Sesión
Al ingresar a la aplicación, el usuario puede crear una cuenta nueva o iniciar sesión con una existente.
Existe una opción para "Mantener sesión iniciada", que permite recordar la cuenta en el navegador.
Al ingresar, el sistema siempre redirige a la pantalla de inicio para evitar conflictos de navegación.

2. Biblioteca (Pantalla Principal)
Es el núcleo de la aplicación. Muestra todos los juegos registrados en formato de tarjetas, incluyendo portada, título, puntuación, horas y estado.
Agregar juego: Hacer clic en el botón flotante inferior. El título es el único campo obligatorio. El botón de la lupa busca la portada automáticamente en Steam.
Editar: Permite modificar los datos de un juego existente.
Eliminar: Aplica la baja lógica. El juego desaparece de la vista del usuario, pero no se borra de la base de datos.
Buscar: La barra superior permite filtrar los juegos por nombre en tiempo real.

3. Dashboard (Estadísticas)
Presenta un resumen visual de la colección: total de juegos, porcentaje de completados, horas totales y promedio de puntuación. Incluye gráficos de distribución por estado, actividad de carga y los géneros más jugados.
4. Mi Perfil y Ranking
En Perfil, el usuario puede personalizar su foto (pegando un enlace de imagen) y ver su rango actual con una barra de progreso.
En Ranking, se muestra la lista completa de rangos y los requisitos para cada uno.

5. Gestión (Solo Administradores)
Los usuarios con rol de administrador tienen acceso a una pestaña adicional donde pueden buscar usuarios por correo y desactivar sus cuentas. La cuenta del administrador principal está protegida y no puede ser desactivada por error.
Notas Técnicas y Arquitectura
Seguridad de contraseñas: Las contraseñas no se almacenan en texto plano. La plataforma Supabase Auth se encarga del hashing mediante el algoritmo bcrypt.
Protección de rutas: El frontend valida el token y el rol del usuario, mientras que el backend verifica la autenticidad del JWT (JSON Web Tokens) en cada petición.
Baja lógica: Implementada en la tabla de juegos mediante un campo booleano llamado activo para preservar la integridad de los datos.
Base de Datos: PostgreSQL alojado en Supabase. El modelo está normalizado (3FN) e incluye relaciones uno a muchos (usuarios-juegos) y muchos a muchos (juegos-géneros mediante tabla pivote).
Tecnologías: Vue 3, Vite, Vue Router, Axios y Chart.js (Frontend). Python 3, FastAPI y Pydantic (Backend).




