<template>
  <div class="app-container">
    <header>
      <h1><i class="fa-solid fa-gamepad"></i> PLAY UP</h1>
      <p>Tu biblioteca personal de videojuegos</p>
    </header>

    <main>
      <!-- Formulario (Agregar / Editar) -->
      <section class="form-section">
        <h2>{{ idEdicion ? 'Editar Juego' : 'Agregar Juego' }}</h2>
        <form @submit.prevent="guardarJuego">
          <input v-model="nuevoJuego.titulo" placeholder="Título del juego" required />
          <input v-model.number="nuevoJuego.puntuacion" type="number" step="0.1" min="1" max="10" placeholder="Puntuación (1-10)" />
          <input v-model.number="nuevoJuego.duracion_horas" type="number" step="0.5" placeholder="Horas jugadas" />
          <input v-model="nuevoJuego.notas" placeholder="Notas (opcional)" />
          
          <select v-model.number="nuevoJuego.estado_id" required>
            <option :value="null" disabled>Seleccioná un estado</option>
            <option :value="1">En curso</option>
            <option :value="2">Terminado</option>
            <option :value="3">Pendiente</option>
            <option :value="4">Abandonado</option>
          </select>

          <button type="submit" :class="{ 'btn-editar': idEdicion }">
            {{ idEdicion ? 'Guardar Cambios' : 'Agregar a la Biblioteca' }}
          </button>
          
          <button v-if="idEdicion" type="button" @click="cancelarEdicion" class="btn-cancelar">
            Cancelar
          </button>
        </form>
      </section>

      <!-- Buscador y Grilla -->
      <section class="biblioteca">
        <div class="header-biblioteca">
          <h2>Mi Biblioteca ({{ juegosFiltrados.length }})</h2>
          <input v-model="busqueda" type="search" placeholder="🔍 Buscar juego..." class="buscador" />
        </div>

        <!-- Reporte de métricas -->
        <div class="reporte-metricas">
          <div class="metrica">
            <span class="metrica-titulo">Total</span>
            <span class="metrica-valor">{{ totalJuegos }}</span>
          </div>
          <div class="metrica">
            <span class="metrica-titulo">Promedio</span>
            <span class="metrica-valor">⭐ {{ promedioPuntuacion }}</span>
          </div>
          <div class="metrica">
            <span class="metrica-titulo">Horas Jugadas</span>
            <span class="metrica-valor">⏱️ {{ totalHoras }}h</span>
          </div>
        </div>

        <div v-if="cargando">Cargando juegos...</div>
        <div v-else-if="juegosFiltrados.length === 0" class="vacio">
          No se encontraron juegos.
        </div>

        <div v-else class="grid-juegos">
          <div v-for="juego in juegosFiltrados" :key="juego.id" class="card-juego">
            <h3>{{ juego.titulo }}</h3>
            <div class="card-info">
              <span><i class="fa-solid fa-star" style="color: #FBBF24;"></i> {{ juego.puntuacion || 'S/N' }}</span>
              <span><i class="fa-solid fa-clock" style="color: #94A3B8;"></i> {{ juego.duracion_horas || 0 }}h</span>
            </div>
            <p class="notas">{{ juego.notas || 'Sin notas' }}</p>
            
            <div class="card-acciones">
              <button @click="prepararEdicion(juego)" class="btn-editar-card">
                <i class="fa-solid fa-pen"></i> Editar
              </button>
              <button @click="eliminarJuego(juego.id)" class="btn-borrar">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/juegos'

const juegos = ref([])
const cargando = ref(true)
const busqueda = ref('')
const idEdicion = ref(null)

const juegoVacio = {
  titulo: '',
  puntuacion: null,
  duracion_horas: null,
  notas: '',
  estado_id: null
}

const nuevoJuego = ref({ ...juegoVacio })

// --- CARGAR DATOS ---
const cargarJuegos = async () => {
  try {
    cargando.value = true
    const respuesta = await axios.get(API_URL)
    juegos.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar juegos:", error)
  } finally {
    cargando.value = false
  }
}

// --- GUARDAR (CREAR O EDITAR) ---
const guardarJuego = async () => {
  try {
    if (idEdicion.value) {
      // Si hay ID, es una edición (PUT)
      await axios.put(`${API_URL}/${idEdicion.value}`, nuevoJuego.value)
    } else {
      // Si no, es un juego nuevo (POST)
      await axios.post(API_URL, nuevoJuego.value)
    }
    limpiarFormulario()
    await cargarJuegos()
  } catch (error) {
    console.error("Error al guardar:", error)
    alert("Hubo un error al guardar el juego")
  }
}

// --- PREPARAR EDICIÓN ---
const prepararEdicion = (juego) => {
  idEdicion.value = juego.id
  nuevoJuego.value = {
    titulo: juego.titulo,
    puntuacion: juego.puntuacion,
    duracion_horas: juego.duracion_horas,
    notas: juego.notas,
    estado_id: juego.estado_id
  }
  window.scrollTo({ top: 0, behavior: 'smooth' }) // Sube al form
}

const cancelarEdicion = () => {
  limpiarFormulario()
}

const limpiarFormulario = () => {
  idEdicion.value = null
  nuevoJuego.value = { ...juegoVacio }
}

// --- ELIMINAR ---
const eliminarJuego = async (id) => {
  if (!confirm('¿Seguro que querés eliminar este juego?')) return
  try {
    await axios.delete(`${API_URL}/${id}`)
    await cargarJuegos()
  } catch (error) {
    console.error("Error al eliminar:", error)
  }
}

// --- BUSCADOR Y MÉTRICAS ---
const juegosFiltrados = computed(() => {
  const termino = busqueda.value.toLowerCase()
  return juegos.value.filter(j => j.titulo.toLowerCase().includes(termino))
})

const totalJuegos = computed(() => juegos.value.length)

const promedioPuntuacion = computed(() => {
  const conPuntuacion = juegos.value.filter(j => j.puntuacion !== null)
  if (conPuntuacion.length === 0) return 0
  const suma = conPuntuacion.reduce((acc, j) => acc + j.puntuacion, 0)
  return (suma / conPuntuacion.length).toFixed(1)
})

const totalHoras = computed(() => {
  return juegos.value.reduce((acc, j) => acc + (j.duracion_horas || 0), 0).toFixed(1)
})

onMounted(() => {
  cargarJuegos()
})
</script>

<style>
:root {
  --fondo-principal: #111827;
  --fondo-tarjeta: #1E293B;
  --azul-principal: #38BDF8;
  --texto-principal: #F8FAFC;
  --texto-secundario: #94A3B8;
  --borde: #334155;
  --rojo: #F87171;
}

body {
  margin: 0;
  font-family: 'Segoe UI', system-ui, sans-serif;
  background-color: var(--fondo-principal);
  color: var(--texto-principal);
}

.app-container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
header { text-align: center; margin-bottom: 3rem; }
header h1 { font-size: 3rem; color: var(--azul-principal); margin-bottom: 0.5rem; }
header p { color: var(--texto-secundario); }

.form-section {
  background: var(--fondo-tarjeta); padding: 1.5rem;
  border-radius: 8px; border: 1px solid var(--borde); margin-bottom: 3rem;
}
form { display: flex; gap: 1rem; flex-wrap: wrap; }
input, select, button {
  padding: 0.75rem; border-radius: 4px; border: 1px solid var(--borde);
  background: var(--fondo-principal); color: white; font-size: 1rem;
}
button {
  background: var(--azul-principal); color: black; font-weight: bold;
  cursor: pointer; border: none; transition: opacity 0.2s;
}
button:hover { opacity: 0.8; }
.btn-cancelar { background: var(--texto-secundario); color: white; }

.header-biblioteca {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;
}
.buscador { width: 300px; }

.reporte-metricas { display: flex; gap: 1rem; margin-bottom: 2rem; }
.metrica {
  flex: 1; background: var(--fondo-tarjeta); padding: 1rem;
  border-radius: 8px; border: 1px solid var(--borde);
  display: flex; flex-direction: column; align-items: center;
}
.metrica-titulo { color: var(--texto-secundario); font-size: 0.9rem; margin-bottom: 0.5rem; }
.metrica-valor { font-size: 1.5rem; font-weight: bold; color: var(--azul-principal); }

.grid-juegos { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; }
.card-juego {
  background: var(--fondo-tarjeta); padding: 1.5rem; border-radius: 8px;
  border: 1px solid var(--borde); box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  display: flex; flex-direction: column;
}
.card-juego h3 { margin-top: 0; color: var(--azul-principal); }
.card-info { display: flex; justify-content: space-between; color: var(--texto-secundario); font-weight: bold; margin-bottom: 1rem; }
.notas { color: var(--texto-secundario); font-size: 0.9rem; font-style: italic; flex-grow: 1; }

.card-acciones { display: flex; gap: 0.5rem; margin-top: 1rem; }
.btn-editar-card { background: var(--azul-principal); flex: 1; padding: 0.5rem; font-size: 0.9rem; }
.btn-borrar { background: var(--rojo); flex: 1; padding: 0.5rem; font-size: 0.9rem; color: white; }
.vacio { text-align: center; color: var(--texto-secundario); font-size: 1.2rem; padding: 3rem; }
</style>