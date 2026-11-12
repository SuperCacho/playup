<template>
  <div class="biblioteca-container">
    <div class="header-biblioteca">
      <h1 class="titulo-pagina">Biblioteca</h1>
      <input v-model="busqueda" type="search" placeholder="🔍 Buscar juego..." class="buscador" />
    </div>

    <button class="fab" @click="abrirFormulario" v-if="!mostrarFormulario">
      <i class="fa-solid fa-plus"></i> <span class="fab-texto">Agregar Juego</span>
    </button>

    <div v-if="mostrarFormulario" class="modal-overlay" @click.self="cerrarFormulario">
      <div class="modal-content glass-panel compact-modal">
        <div class="modal-header">
          <h2>{{ idEdicion ? '✏️ Editar Juego' : 'Agregar Juego' }}</h2>
          <button class="btn-cerrar" @click="cerrarFormulario"><i class="fa-solid fa-xmark"></i></button>
        </div>
        
        <form @submit.prevent="guardarJuego">
          <div class="input-group col-span-2">
            <label>Título del juego *</label>
            <div style="display: flex; gap: 8px;">
              <input v-model="nuevoJuego.titulo" placeholder="Ej: Elden Ring" required style="flex: 1;" />
              <button type="button" @click="buscarPortada" class="btn-buscar" title="Buscar Portada en Steam"><i class="fa-solid fa-magnifying-glass"></i></button>
            </div>
          </div>

          <div class="input-group col-span-2">
            <label>Portada (URL)</label>
            <input v-model="nuevoJuego.portada_url" placeholder="Se autocompleta o pegá un link" />
          </div>

          <div class="input-group"><label>Puntuación (1-10)</label><input v-model.number="nuevoJuego.puntuacion" type="number" step="0.1" min="1" max="10" /></div>
          <div class="input-group"><label>Horas jugadas</label><input v-model.number="nuevoJuego.duracion_horas" type="number" step="0.5" /></div>
          
          <!-- DROPDOWN CUSTOM: ESTADO -->
          <div class="input-group" style="position: relative;">
            <label>Estado *</label>
            <div class="custom-select" @click="toggleMenu('estado')">
              <span>{{ obtenerNombre('estados', nuevoJuego.estado_id) || 'Seleccioná' }}</span>
              <i class="fa-solid fa-chevron-down" :style="{ transform: menuAbierto === 'estado' ? 'rotate(180deg)' : 'rotate(0)' }"></i>
            </div>
            <div v-if="menuAbierto === 'estado'" class="menu-desplegable glass-panel">
              <label v-for="est in catalogos.estados" :key="est.id" class="menu-item" @click="seleccionar('estado_id', est.id)">
                {{ est.nombre }}
              </label>
            </div>
          </div>

          <!-- DROPDOWN CUSTOM: CATEGORÍA -->
          <div class="input-group" style="position: relative;">
            <label>Categoría</label>
            <div class="custom-select" @click="toggleMenu('categoria')">
              <span>{{ obtenerNombre('categorias', nuevoJuego.categoria_id) || 'Seleccioná' }}</span>
              <i class="fa-solid fa-chevron-down" :style="{ transform: menuAbierto === 'categoria' ? 'rotate(180deg)' : 'rotate(0)' }"></i>
            </div>
            <div v-if="menuAbierto === 'categoria'" class="menu-desplegable glass-panel">
              <label v-for="cat in catalogos.categorias" :key="cat.id" class="menu-item" @click="seleccionar('categoria_id', cat.id)">
                {{ cat.nombre }}
              </label>
            </div>
          </div>

          <!-- DROPDOWN CUSTOM: OPINIÓN -->
          <div class="input-group" style="position: relative;">
            <label>Opinión</label>
            <div class="custom-select" @click="toggleMenu('opinion')">
              <span>{{ obtenerNombre('opiniones', nuevoJuego.opinion_id) || 'Seleccioná' }}</span>
              <i class="fa-solid fa-chevron-down" :style="{ transform: menuAbierto === 'opinion' ? 'rotate(180deg)' : 'rotate(0)' }"></i>
            </div>
            <div v-if="menuAbierto === 'opinion'" class="menu-desplegable glass-panel">
              <label v-for="op in catalogos.opiniones" :key="op.id" class="menu-item" @click="seleccionar('opinion_id', op.id)">
                {{ op.nombre }}
              </label>
            </div>
          </div>

          <!-- DROPDOWN CUSTOM: GÉNEROS (Múltiple) -->
          <div class="input-group" style="position: relative;">
            <label>Géneros</label>
            <div class="custom-select" @click="toggleMenu('generos')">
              <span v-if="nuevoJuego.generos.length === 0">Seleccionar...</span>
              <span v-else>{{ nuevoJuego.generos.length }} seleccionados</span>
              <i class="fa-solid fa-chevron-down" :style="{ transform: menuAbierto === 'generos' ? 'rotate(180deg)' : 'rotate(0)' }"></i>
            </div>
            <!-- max-height: 90px limita a mostrar solo 2 items -->
            <div v-if="menuAbierto === 'generos'" class="menu-desplegable glass-panel limited-height">
              <label v-for="gen in catalogos.generos" :key="gen.id" class="menu-item">
                <input type="checkbox" :value="gen.id" v-model="nuevoJuego.generos" /> {{ gen.nombre }}
              </label>
            </div>
          </div>

          <div class="input-group col-span-2">
            <label>Notas / Observaciones</label>
            <textarea v-model="nuevoJuego.notas" placeholder="¿Qué te pareció?" rows="2"></textarea>
          </div>

          <div class="form-acciones col-span-2">
            <button type="submit" class="btn-primary">{{ idEdicion ? 'Guardar Cambios' : 'Agregar' }}</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="cargando" class="vacio">Cargando...</div>
    <div v-else-if="juegosFiltrados.length === 0" class="vacio">No hay juegos.</div>
    <div v-else class="grid-juegos">
      <div v-for="juego in juegosFiltrados" :key="juego.id" class="card-juego glass-panel">
        <img :src="juego.portada_url || `https://placehold.co/600x400/1e293b/38BDF8?text=${encodeURIComponent(juego.titulo)}`" class="portada" alt="Portada" @error="(e) => e.target.src = `https://placehold.co/600x400/1e293b/38BDF8?text=${encodeURIComponent(juego.titulo)}`" />
        <div class="card-body">
          <h3>{{ juego.titulo }}</h3>
          <div class="card-info">
            <span><i class="fa-solid fa-star" style="color: #FBBF24;"></i> {{ juego.puntuacion || 'S/N' }}</span>
            <span><i class="fa-solid fa-clock" style="color: #94A3B8;"></i> {{ juego.duracion_horas || 0 }}h</span>
          </div>
          <div class="tags-generos"><span v-for="g in juego.generos" :key="g.id" class="tag">{{ g.nombre }}</span></div>
          <div class="tags-extra">
            <span v-if="juego.categoria_id" class="tag-extra"><i class="fa-solid fa-layer-group"></i> {{ obtenerNombre('categorias', juego.categoria_id) }}</span>
            <span v-if="juego.opinion_id" class="tag-extra"><i class="fa-regular fa-face-smile"></i> {{ obtenerNombre('opiniones', juego.opinion_id) }}</span>
          </div>
          <p class="notas-card" v-if="juego.notas">{{ juego.notas }}</p>
          <div class="card-acciones">
            <button @click="prepararEdicion(juego)" class="btn-editar-card"><i class="fa-solid fa-pen"></i> Editar</button>
            <button @click="eliminarJuego(juego.id)" class="btn-borrar"><i class="fa-solid fa-trash"></i></button>
          </div>
        </div>
      </div>
    </div>
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
const mostrarFormulario = ref(false)
const menuAbierto = ref(null) // Controla qué dropdown está abierto
const catalogos = ref({ estados: [], generos: [], categorias: [], opiniones: [] })

const juegoVacio = { titulo: '', portada_url: '', puntuacion: null, duracion_horas: null, estado_id: null, categoria_id: null, opinion_id: null, generos: [], notas: '' }
const nuevoJuego = ref({ ...juegoVacio })

const cargarTodo = async () => {
  try {
    const [resJuegos, resCatalogos] = await Promise.all([axios.get(`${API_URL}/`), axios.get(`${API_URL}/catalogos`)])
    juegos.value = resJuegos.data
    catalogos.value = resCatalogos.data
  } catch (error) { console.error(error) } finally { cargando.value = false }
}

const abrirFormulario = () => { limpiarFormulario(); mostrarFormulario.value = true }
const cerrarFormulario = () => { mostrarFormulario.value = false; menuAbierto.value = null; limpiarFormulario() }

const guardarJuego = async () => {
  try {
    if (idEdicion.value) await axios.put(`${API_URL}/${idEdicion.value}`, nuevoJuego.value)
    else await axios.post(`${API_URL}/`, nuevoJuego.value)
    cerrarFormulario()
    await cargarTodo()
  } catch (error) { alert("Error al guardar") }
}

const prepararEdicion = (juego) => {
  idEdicion.value = juego.id
  nuevoJuego.value = { ...juego, generos: juego.generos ? juego.generos.map(g => g.id) : [] }
  mostrarFormulario.value = true
}

const limpiarFormulario = () => { idEdicion.value = null; nuevoJuego.value = { ...juegoVacio, generos: [] } }
const eliminarJuego = async (id) => {
  if (!confirm('¿Eliminar juego?')) return
  try { await axios.delete(`${API_URL}/${id}`); await cargarTodo() } catch (error) { console.error(error) }
}

const buscarPortada = async () => {
  if (!nuevoJuego.value.titulo) return alert("Escribí un título primero");
  try {
    const res = await axios.get(`${API_URL}/buscar-imagen/${nuevoJuego.value.titulo}`);
    if (res.data.encontrado) nuevoJuego.value.portada_url = res.data.portada_url;
    else alert("No se encontró la portada en Steam. Podés pegar el link a mano.");
  } catch (error) { console.error(error); }
}

// Lógica de los desplegables custom
const toggleMenu = (menu) => { menuAbierto.value = menuAbierto.value === menu ? null : menu }
const seleccionar = (campo, id) => { nuevoJuego.value[campo] = id; menuAbierto.value = null }
const obtenerNombre = (tabla, id) => catalogos.value[tabla]?.find(item => item.id === id)?.nombre || ''

const juegosFiltrados = computed(() => juegos.value.filter(j => j.titulo.toLowerCase().includes(busqueda.value.toLowerCase())))

onMounted(() => { cargarTodo() })
</script>

<style scoped>
.titulo-pagina { color: var(--azul-principal); font-weight: 800; }
.header-biblioteca { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.buscador { width: 300px; padding: 0.75rem; border-radius: 20px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6); color: white; }
.fab { position: fixed; bottom: 2rem; right: 2rem; background: var(--azul-principal); color: black; border: none; padding: 1rem 2rem; border-radius: 30px; font-weight: 800; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.5); transition: 0.3s; z-index: 50; display: flex; align-items: center; gap: 10px;}
.fab:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.8); }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(5px); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem;}
/* MODAL MÁS COMPACTO */
.compact-modal { width: 100%; max-width: 600px; padding: 1.5rem 2rem; border-radius: 16px; background: #1e293b; animation: slideUp 0.3s ease-out; max-height: 95vh; overflow-y: auto; }
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.btn-cerrar { background: transparent; border: none; color: var(--rojo); font-size: 1.5rem; cursor: pointer; }

form { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
.col-span-2 { grid-column: span 2; }
.input-group { display: flex; flex-direction: column; gap: 0.3rem; }
.input-group label { color: var(--texto-secundario); font-size: 0.8rem; font-weight: 600; }
input, textarea { padding: 0.6rem; border-radius: 8px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6); color: white; font-family: inherit; width: 100%; box-sizing: border-box;}
textarea { resize: vertical; min-height: 60px; }
.form-acciones { display: flex; justify-content: flex-end; margin-top: 0.5rem; }
.btn-primary { background: var(--azul-principal); color: black; font-weight: 800; padding: 0.6rem 1.5rem; border-radius: 8px; border: none; cursor: pointer; }
.btn-buscar { background: var(--azul-principal); color: black; border: none; border-radius: 8px; padding: 0 1rem; cursor: pointer; transition: 0.3s; }
.btn-buscar:hover { opacity: 0.8; }

/* CUSTOM SELECTS (Reemplaza a los <select> nativos) */
.custom-select { padding: 0.6rem; border-radius: 8px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6); color: white; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem;}
.custom-select i { font-size: 0.8rem; transition: transform 0.3s; }
.menu-desplegable { position: absolute; top: 100%; left: 0; right: 0; z-index: 1200; margin-top: 5px; max-height: 180px; overflow-y: auto; border-radius: 8px; background: #1e293b; border: 1px solid var(--borde); box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
/* Altura limitada para mostrar solo 2 items en géneros */
.limited-height { max-height: 95px; } 
.menu-desplegable::-webkit-scrollbar { width: 6px; }
.menu-desplegable::-webkit-scrollbar-thumb { background: var(--azul-principal); border-radius: 3px; }
.menu-item { display: flex; align-items: center; gap: 10px; padding: 10px; cursor: pointer; color: white; font-size: 0.9rem; transition: 0.2s; border-bottom: 1px solid rgba(255,255,255,0.05);}
.menu-item:hover { background: rgba(56, 189, 248, 0.1); }
.menu-item input { width: auto; }

.grid-juegos { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; }
.card-juego { border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; transition: 0.3s; }
.card-juego:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.2); }
.portada { width: 100%; height: 150px; object-fit: cover; }
.card-body { padding: 1rem; display: flex; flex-direction: column; flex: 1;}
.card-body h3 { margin: 0 0 0.5rem 0; color: var(--azul-principal); font-size: 1.1rem;}
.card-info { display: flex; justify-content: space-between; color: var(--texto-secundario); font-weight: 600; margin-bottom: 0.5rem; }
.tags-generos, .tags-extra { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
.tag { background: rgba(56, 189, 248, 0.15); color: var(--azul-principal); font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.tag-extra { background: rgba(255, 255, 255, 0.1); color: #cbd5e1; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
.notas-card { font-size: 0.85rem; color: var(--texto-secundario); font-style: italic; margin-bottom: 1rem; border-left: 2px solid var(--borde); padding-left: 8px;}
.card-acciones { display: flex; gap: 0.5rem; margin-top: auto; }
.btn-editar-card { background: rgba(56, 189, 248, 0.1); color: var(--azul-principal); border: 1px solid var(--azul-principal); flex: 1; padding: 0.5rem; border-radius: 6px; cursor: pointer; transition: 0.3s;}
.btn-editar-card:hover { background: var(--azul-principal); color: black; }
.btn-borrar { background: rgba(248, 113, 113, 0.1); color: var(--rojo); border: 1px solid var(--rojo); flex: 1; padding: 0.5rem; border-radius: 6px; cursor: pointer; transition: 0.3s;}
.btn-borrar:hover { background: var(--rojo); color: white; }
.vacio { text-align: center; color: var(--texto-secundario); padding: 3rem; font-size: 1.2rem;}

@media (max-width: 768px) {
  form { grid-template-columns: 1fr; }
  .col-span-2 { grid-column: span 1; }
  .header-biblioteca { flex-direction: column; gap: 1rem; align-items: stretch; margin-bottom: 1.5rem;}
  .buscador { width: 100%; }
  .compact-modal { padding: 1.5rem; max-height: 95vh; }
  .fab { bottom: 80px; right: 1rem; padding: 1rem; border-radius: 50%; }
  .fab-texto { display: none; }
  .grid-juegos { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
}
</style>