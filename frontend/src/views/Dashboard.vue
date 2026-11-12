<template>
  <div class="dashboard-container">
    <h1 class="titulo-pagina">Dashboard General</h1>
    
    <div v-if="cargando" class="vacio">Calculando métricas...</div>
    
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
      </div>

      <div class="graficos-grid">
        <div class="grafico-card glass-panel">
          <h2>Distribución por Estado</h2>
          <div class="canvas-container">
            <Doughnut v-if="datosEstados.labels.length" :data="datosEstados" :options="opcionesDoughnut" />
            <p v-else class="vacio">No hay datos</p>
          </div>
        </div>

        <!-- NUEVO GRÁFICO DE LÍNEA (Actividad Reciente) -->
        <div class="grafico-card glass-panel">
          <h2>Juegos Añadidos (Últimos 6 Meses)</h2>
          <div class="canvas-container">
            <Line v-if="datosActividad.labels.length" :data="datosActividad" :options="opcionesLine" />
            <p v-else class="vacio">No hay datos suficientes</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'
import { Doughnut, Line } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, ArcElement, LineElement, PointElement, CategoryScale, LinearScale)

const API_URL = 'http://127.0.0.1:8000/api/juegos'
const juegos = ref([])
const catalogos = ref({ estados: [], generos: [] })
const cargando = ref(true)

onMounted(async () => {
  try {
    const [resJuegos, resCatalogos] = await Promise.all([axios.get(`${API_URL}/`), axios.get(`${API_URL}/catalogos`)])
    juegos.value = resJuegos.data
    catalogos.value = resCatalogos.data
  } catch (error) { console.error(error) } finally { cargando.value = false }
})

const totalJuegos = computed(() => juegos.value.length)
const totalHoras = computed(() => juegos.value.reduce((acc, j) => acc + (j.duracion_horas || 0), 0).toFixed(1))
const porcentajeCompletados = computed(() => {
  if (totalJuegos.value === 0) return 0
  return Math.round((juegos.value.filter(j => j.estado_id === 2).length / totalJuegos.value) * 100)
})

// Gráfico de Dona (Estados)
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

// Gráfico de Línea (Actividad por fecha de creación)
const datosActividad = computed(() => {
  const conteoFechas = {}
  // Agrupamos por mes/año (ej: "Oct 2023")
  juegos.value.forEach(j => {
    if(j.creado_en) {
      const fecha = new Date(j.creado_en)
      const mes = fecha.toLocaleString('es-ES', { month: 'short', year: 'numeric' })
      conteoFechas[mes] = (conteoFechas[mes] || 0) + 1
    }
  })
  
  // Ordenamos los meses (para simplificar, orden alfabético, aunque lo ideal sería por fecha real)
  const fechas = Object.keys(conteoFechas).reverse()
  
  return {
    labels: fechas,
    datasets: [{
      label: 'Juegos agregados',
      data: fechas.map(f => conteoFechas[f]),
      borderColor: '#38BDF8',
      backgroundColor: 'rgba(56, 189, 248, 0.2)',
      tension: 0.4, // Hace la línea curva
      fill: true
    }]
  }
})

const opcionesDoughnut = { responsive: true, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
const opcionesLine = { 
  responsive: true, plugins: { legend: { display: false } },
  scales: { x: { ticks: { color: '#94A3B8' }, grid: { display: false } }, y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } } }
}
</script>

<style scoped>
.titulo-pagina { color: var(--azul-principal); margin-bottom: 2rem; font-weight: 800; }
.metricas-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.metrica-card { padding: 1.5rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: 0.3s; }
.metrica-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
.metrica-card h3 { margin: 0; font-size: 2rem; color: var(--texto-principal); font-weight: 800;}
.metrica-card p { margin: 0; color: var(--texto-secundario); font-size: 0.9rem; }
.metrica-card i { font-size: 2.5rem; }
.icono-azul { color: var(--azul-principal); }
.icono-verde { color: var(--verde); }
.icono-amarillo { color: var(--amarillo); }
.graficos-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.grafico-card { padding: 1.5rem; border-radius: 12px; }
.grafico-card h2 { margin-top: 0; font-size: 1.1rem; color: var(--texto-principal); margin-bottom: 1.5rem; border-bottom: 1px solid var(--borde); padding-bottom: 10px;}
.canvas-container { height: 250px; position: relative; display: flex; justify-content: center; align-items: center; }

@media (max-width: 900px) {
  .graficos-grid { grid-template-columns: 1fr; }
}
</style>