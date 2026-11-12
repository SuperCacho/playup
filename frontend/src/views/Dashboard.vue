<template>
  <div class="dashboard-container">
    <h1 class="titulo-pagina">Dashboard General</h1>
    
    <div v-if="cargando" class="vacio" style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
  <span class="spinner" style="width: 40px; height: 40px; border-width: 4px; border-top-color: var(--azul-principal);"></span>
  Calculando métricas...
</div>
    
    <div v-else>
      <div class="metricas-grid">
        <div class="metrica-card glass-panel">
          <i class="fa-solid fa-gamepad icono-azul"></i>
          <div><h3>{{ totalJuegos }}</h3><p>Juegos Totales</p></div>
        </div>
        <div class="metrica-card glass-panel">
          <i class="fa-solid fa-check-circle icono-verde"></i>
          <div><h3>{{ porcentajeCompletados }}%</h3><p>Completados</p></div>
        </div>
        <div class="metrica-card glass-panel">
          <i class="fa-solid fa-clock icono-amarillo"></i>
          <div><h3>{{ totalHoras }}h</h3><p>Horas Jugadas</p></div>
        </div>
        <div class="metrica-card glass-panel">
          <i class="fa-solid fa-star icono-azul"></i>
          <div><h3>{{ promedioPuntuacion }}</h3><p>Promedio Puntuación</p></div>
        </div>
      </div>

      <div class="graficos-grid-2">
        <div class="grafico-card glass-panel">
          <h2>Distribución por Estado</h2>
          <div class="canvas-container">
            <Doughnut v-if="datosEstados.labels.length" :data="datosEstados" :options="opcionesDoughnut" />
            <p v-else class="vacio">No hay datos</p>
          </div>
        </div>

        <div class="grafico-card glass-panel">
          <h2>Juegos Añadidos (Actividad)</h2>
          <div class="canvas-container">
            <Line v-if="datosActividad.labels.length" :data="datosActividad" :options="opcionesLine" />
            <p v-else class="vacio">No hay datos suficientes</p>
          </div>
        </div>
      </div>

      <div class="graficos-grid-2">
        <div class="grafico-card glass-panel">
          <h2>Distribución de Puntuaciones</h2>
          <div class="canvas-container">
            <Bar v-if="datosPuntuaciones.labels.length" :data="datosPuntuaciones" :options="opcionesBarVertical" />
            <p v-else class="vacio">No hay juegos puntuados</p>
          </div>
        </div>

        <div class="grafico-card glass-panel">
          <h2>Top 5 Géneros (por Horas)</h2>
          <div class="canvas-container">
            <Bar v-if="datosTopGeneros.labels.length" :data="datosTopGeneros" :options="opcionesBarHorizontal" />
            <p v-else class="vacio">No hay horas registradas</p>
          </div>
        </div>
      </div>

      <div class="graficos-grid-2">
        <div class="grafico-card glass-panel">
          <h2><i class="fa-solid fa-trophy" style="color:#FBBF24;"></i> Salón de la Fama (Top 5)</h2>
          <div class="top-juegos-lista">
            <div v-for="(juego, index) in topJuegos" :key="juego.id" class="top-juego-item">
              <span class="top-numero" :class="'top-' + (index + 1)">#{{ index + 1 }}</span>
              <img :src="obtenerPortada(juego)" class="top-portada" alt="Portada" />
              <div class="top-info">
                <h4>{{ juego.titulo }}</h4>
                <p><i class="fa-solid fa-star" style="color: #FBBF24;"></i> {{ juego.puntuacion }} / 10</p>
              </div>
            </div>
            <p v-if="topJuegos.length === 0" class="vacio">Todavía no hay juegos puntuados.</p>
          </div>
        </div>

        <div class="grafico-card glass-panel">
          <h2>Resumen de Colección</h2>
          <div class="resumen-grid">
            <div class="resumen-item">
              <h3><i class="fa-solid fa-heart" style="color: #F87171;"></i> Favoritos</h3>
              <p>{{ conteoOpiniones['Favorito'] || 0 }} juegos</p>
            </div>
            <div class="resumen-item">
              <h3><i class="fa-solid fa-face-smile" style="color: #4ADE80;"></i> Me Gustó</h3>
              <p>{{ conteoOpiniones['Me gustó'] || 0 }} juegos</p>
            </div>
            <div class="resumen-item">
              <h3><i class="fa-solid fa-users" style="color: #60A5FA;"></i> Multijugador</h3>
              <p>{{ conteoCategorias['Multijugador'] || 0 }} juegos</p>
            </div>
            <div class="resumen-item">
              <h3><i class="fa-solid fa-user" style="color: #A78BFA;"></i> Un Jugador</h3>
              <p>{{ conteoCategorias['Con un final'] || 0 }} juegos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale, LineElement, PointElement
} from 'chart.js'
import { Doughnut, Line, Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale, LineElement, PointElement)

const API_URL = 'http://127.0.0.1:8000/api/juegos'
const juegos = ref([])
const catalogos = ref({ estados: [], generos: [], categorias: [], opiniones: [] })
const cargando = ref(true)

onMounted(async () => {
  try {
    const [resJuegos, resCatalogos] = await Promise.all([axios.get(`${API_URL}/`), axios.get(`${API_URL}/catalogos`)])
    juegos.value = resJuegos.data
    catalogos.value = resCatalogos.data
  } catch (error) {
    console.error(error)
  } finally {
    cargando.value = false
  }
})

const totalJuegos = computed(() => juegos.value.length)
const totalHoras = computed(() => juegos.value.reduce((acc, j) => acc + (j.duracion_horas || 0), 0).toFixed(1))
const promedioPuntuacion = computed(() => {
  const conP = juegos.value.filter(j => j.puntuacion !== null)
  if (conP.length === 0) return 0
  return (conP.reduce((acc, j) => acc + j.puntuacion, 0) / conP.length).toFixed(1)
})
const porcentajeCompletados = computed(() => {
  if (totalJuegos.value === 0) return 0
  return Math.round((juegos.value.filter(j => j.estado_id === 2).length / totalJuegos.value) * 100)
})

const datosEstados = computed(() => {
  const conteo = {}
  juegos.value.forEach(j => { conteo[j.estado_id] = (conteo[j.estado_id] || 0) + 1 })
  const labels = []; const data = []; const backgroundColor = []
  const colores = { 1: '#60A5FA', 2: '#4ADE80', 3: '#FBBF24', 4: '#F87171' }
  catalogos.value.estados.forEach(est => {
    if (conteo[est.id]) { labels.push(est.nombre); data.push(conteo[est.id]); backgroundColor.push(colores[est.id]) }
  })
  return { labels, datasets: [{ data, backgroundColor, borderWidth: 0 }] }
})

const datosActividad = computed(() => {
  const conteoFechas = {}
  juegos.value.forEach(j => {
    if(j.creado_en) {
      const fecha = new Date(j.creado_en)
      const mes = fecha.toLocaleString('es-ES', { month: 'short', year: 'numeric' })
      conteoFechas[mes] = (conteoFechas[mes] || 0) + 1
    }
  })
  const fechas = Object.keys(conteoFechas).reverse()
  return {
    labels: fechas,
    datasets: [{ label: 'Juegos agregados', data: fechas.map(f => conteoFechas[f]), borderColor: '#38BDF8', backgroundColor: 'rgba(56, 189, 248, 0.2)', tension: 0.4, fill: true }]
  }
})

const datosPuntuaciones = computed(() => {
  const conteo = { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0 }
  let hayDatos = false
  juegos.value.forEach(j => {
    if (j.puntuacion) {
      const nota = Math.round(j.puntuacion)
      if (nota >= 1 && nota <= 10) { conteo[nota]++; hayDatos = true }
    }
  })
  if (!hayDatos) return { labels: [], datasets: [] }
  return { labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], datasets: [{ label: 'Cantidad de juegos', data: Object.values(conteo), backgroundColor: '#38BDF8', borderRadius: 6 }] }
})

const datosTopGeneros = computed(() => {
  const horasPorGenero = {}
  juegos.value.forEach(j => {
    if (j.generos && j.duracion_horas) {
      j.generos.forEach(g => { horasPorGenero[g.nombre] = (horasPorGenero[g.nombre] || 0) + j.duracion_horas })
    }
  })
  const ordenados = Object.keys(horasPorGenero).map(nombre => ({ nombre, horas: horasPorGenero[nombre] })).sort((a, b) => b.horas - a.horas).slice(0, 5)
  if (ordenados.length === 0) return { labels: [], datasets: [] }
  return { labels: ordenados.map(o => o.nombre), datasets: [{ label: 'Horas jugadas', data: ordenados.map(o => o.horas), backgroundColor: ['#38BDF8', '#4ADE80', '#FBBF24', '#F87171', '#A78BFA'], borderRadius: 6 }] }
})

const topJuegos = computed(() => [...juegos.value].filter(j => j.puntuacion != null).sort((a, b) => b.puntuacion - a.puntuacion).slice(0, 5))

const conteoOpiniones = computed(() => {
  const conteo = {}
  juegos.value.forEach(j => {
    if (j.opinion_id) {
      const op = catalogos.value.opiniones.find(o => o.id === j.opinion_id)
      if (op) conteo[op.nombre] = (conteo[op.nombre] || 0) + 1
    }
  })
  return conteo
})

const conteoCategorias = computed(() => {
  const conteo = {}
  juegos.value.forEach(j => {
    if (j.categoria_id) {
      const cat = catalogos.value.categorias.find(c => c.id === j.categoria_id)
      if (cat) conteo[cat.nombre] = (conteo[cat.nombre] || 0) + 1
    }
  })
  return conteo
})

const obtenerPortada = (juego) => juego.portada_url || `https://placehold.co/150x100/1e293b/38BDF8?text=${encodeURIComponent(juego.titulo.substring(0, 10))}`

const opcionesDoughnut = { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
const opcionesLine = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#94A3B8' }, grid: { display: false } }, y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } } } }
const opcionesBarVertical = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#94A3B8' }, grid: { display: false } }, y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } } } }
const opcionesBarHorizontal = { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }, y: { ticks: { color: '#F8FAFC', font: {weight: 'bold'} }, grid: { display: false } } } }
</script>

<style scoped>
.titulo-pagina { color: var(--azul-principal); margin-bottom: 2rem; font-weight: 800; }
.vacio { text-align: center; color: var(--texto-secundario); }
.metricas-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
.metrica-card { padding: 1.5rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: 0.3s; }
.metrica-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
.metrica-card h3 { margin: 0; font-size: 2rem; color: var(--texto-principal); font-weight: 800;}
.metrica-card p { margin: 0; color: var(--texto-secundario); font-size: 0.9rem; }
.metrica-card i { font-size: 2.5rem; }
.icono-azul { color: var(--azul-principal); }
.icono-verde { color: var(--verde); }
.icono-amarillo { color: var(--amarillo); }
.graficos-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
.grafico-card { padding: 1.5rem; border-radius: 12px; }
.grafico-card h2 { margin-top: 0; font-size: 1.1rem; color: var(--texto-principal); margin-bottom: 1.5rem; border-bottom: 1px solid var(--borde); padding-bottom: 10px; display: flex; align-items: center; gap: 8px;}
.canvas-container { height: 250px; position: relative; }
.top-juegos-lista { display: flex; flex-direction: column; gap: 10px; }
.top-juego-item { display: flex; align-items: center; gap: 15px; background: rgba(15, 23, 42, 0.4); padding: 10px; border-radius: 8px; transition: 0.3s; }
.top-juego-item:hover { background: rgba(56, 189, 248, 0.1); transform: translateX(5px); }
.top-numero { font-size: 1.5rem; font-weight: 800; color: var(--texto-secundario); width: 30px; text-align: center; }
.top-1 { color: #FBBF24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.5); }
.top-2 { color: #94A3B8; }
.top-3 { color: #B45309; }
.top-portada { width: 80px; height: 45px; object-fit: cover; border-radius: 4px; border: 1px solid var(--borde); }
.top-info h4 { margin: 0; color: white; font-size: 1rem; }
.top-info p { margin: 2px 0 0 0; color: var(--texto-secundario); font-size: 0.85rem; font-weight: bold; }
.resumen-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.resumen-item { background: rgba(15, 23, 42, 0.4); padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid var(--borde);}
.resumen-item h3 { margin: 0 0 5px 0; font-size: 0.95rem; color: var(--texto-principal); display: flex; align-items: center; justify-content: center; gap: 8px;}
.resumen-item p { margin: 0; font-size: 1.2rem; font-weight: 800; color: var(--azul-principal); }
@media (max-width: 900px) { .graficos-grid-2 { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .metricas-grid { grid-template-columns: 1fr 1fr; } .metrica-card { padding: 1rem; flex-direction: column; text-align: center; } .metrica-card h3 { font-size: 1.5rem; } .resumen-grid { grid-template-columns: 1fr; } }
</style>