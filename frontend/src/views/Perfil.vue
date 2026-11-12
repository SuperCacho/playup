<template>
  <div class="perfil-container">
    <h1 class="titulo-pagina">Mi Perfil</h1>
    
    <div class="perfil-card glass-panel">
      <div class="avatar-container" :style="{ borderColor: rangoActual.color, boxShadow: `0 0 30px ${rangoActual.color}80` }">
        <img v-if="fotoPerfil" :src="fotoPerfil" class="avatar-img" />
        <i v-else class="fa-solid fa-user-astronaut avatar-icon" :style="{ color: rangoActual.color }"></i>
      </div>
      
      <h2>Coleccionista Gamer</h2>
      <p class="rango-nombre" :style="{ color: rangoActual.color, textShadow: `0 0 10px ${rangoActual.color}80` }">
        {{ rangoActual.nombre }}
      </p>
      
      <div class="perfil-stats">
        <div class="stat"><span class="stat-valor">{{ totalJuegos }}</span><span class="stat-nombre">Juegos</span></div>
        <div class="stat"><span class="stat-valor">{{ totalHoras }}h</span><span class="stat-nombre">Jugadas</span></div>
      </div>

      <div class="progreso-container" v-if="rangoActual.id < 10">
        <div class="progreso-texto">
          <span>Progreso al siguiente rango</span>
          <span>{{ totalHoras }}h / {{ siguienteRango.horas }}h</span>
        </div>
        <div class="barra-fondo">
          <div class="barra-progreso" :style="{ width: porcentajeProgreso + '%', background: rangoActual.color }"></div>
        </div>
        <p class="falta-texto">
          ¡Te faltan <strong>{{ siguienteRango.horas - totalHoras }} horas</strong> y <strong>{{ siguienteRango.juegos - totalJuegos }} juegos</strong> para ser <strong>{{ siguienteRango.nombre }}</strong>!
        </p>
      </div>
      <div class="progreso-container" v-else>
        <p class="falta-texto" style="color: var(--amarillo); font-weight: bold; font-size: 1.1rem;">
          ¡Has alcanzado el rango máximo! 🏆
        </p>
      </div>

      <div class="cambiar-foto">
        <input v-model="fotoPerfil" type="url" placeholder="Pega la URL de tu foto..." />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/juegos'
const juegos = ref([])
const fotoPerfil = ref(localStorage.getItem('fotoPerfil') || '')

watch(fotoPerfil, (val) => { localStorage.setItem('fotoPerfil', val) })

onMounted(async () => {
  try { const res = await axios.get(`${API_URL}/`); juegos.value = res.data } catch (e) { console.error(e) }
})

const totalJuegos = computed(() => juegos.value.length)
const totalHoras = computed(() => juegos.value.reduce((acc, j) => acc + (j.duracion_horas || 0), 0))

const RANGOS = [
  { id: 1, nombre: 'Novato', horas: 500, juegos: 50, color: '#94A3B8' },
  { id: 2, nombre: 'Aprendiz', horas: 1000, juegos: 100, color: '#A78BFA' },
  { id: 3, nombre: 'Jugador', horas: 1500, juegos: 150, color: '#60A5FA' },
  { id: 4, nombre: 'Veterano', horas: 2000, juegos: 200, color: '#34D399' },
  { id: 5, nombre: 'Experto', horas: 2500, juegos: 250, color: '#FBBF24' },
  { id: 6, nombre: 'Élite', horas: 3000, juegos: 300, color: '#F97316' },
  { id: 7, nombre: 'Maestro', horas: 4000, juegos: 400, color: '#F87171' },
  { id: 8, nombre: 'Gran Maestro', horas: 5000, juegos: 500, color: '#EC4899' },
  { id: 9, nombre: 'Leyenda', horas: 7500, juegos: 750, color: '#8B5CF6' },
  { id: 10, nombre: 'Dios Gamer', horas: 10000, juegos: 1000, color: '#38BDF8' }
]

const rangoActual = computed(() => {
  let actual = { id: 0, nombre: 'Sin Rango', color: '#94A3B8', horas: 0, juegos: 0 }
  for (let r of RANGOS) {
    if (totalHoras.value >= r.horas && totalJuegos.value >= r.juegos) {
      actual = r
    }
  }
  return actual
})

const siguienteRango = computed(() => {
  if (rangoActual.value.id === 10) return rangoActual.value
  return RANGOS.find(r => r.id === rangoActual.value.id + 1)
})

const porcentajeProgreso = computed(() => {
  if (rangoActual.value.id === 10) return 100
  if (rangoActual.value.id === 0) return 0
  
  const ptsActual = totalHoras.value - rangoActual.value.horas
  const ptsNecesarios = siguienteRango.value.horas - rangoActual.value.horas
  return Math.min(Math.round((ptsActual / ptsNecesarios) * 100), 100)
})
</script>

<style scoped>
.titulo-pagina { color: var(--azul-principal); margin-bottom: 2rem; font-weight: 800; }
.perfil-container { max-width: 600px; margin: 0 auto; }
.perfil-card { padding: 3rem 2rem; border-radius: 16px; text-align: center; }

.avatar-container { width: 120px; height: 120px; margin: 0 auto 1rem auto; border-radius: 50%; background: var(--fondo-principal); display: flex; justify-content: center; align-items: center; border: 3px solid; overflow: hidden; transition: 0.5s; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-icon { font-size: 4rem; transition: 0.5s; }

h2 { margin: 0; color: white; font-size: 1.5rem; }
.rango-nombre { font-size: 1.2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; margin-top: 0.5rem; transition: 0.5s; }

.perfil-stats { display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; border-top: 1px solid var(--borde); border-bottom: 1px solid var(--borde); padding: 1.5rem 0; }
.stat { display: flex; flex-direction: column; }
.stat-valor { font-size: 1.5rem; font-weight: 800; color: white; }
.stat-nombre { font-size: 0.8rem; color: var(--texto-secundario); text-transform: uppercase; }

.progreso-container { text-align: left; margin-bottom: 2rem; }
.progreso-texto { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--texto-secundario); margin-bottom: 0.5rem; font-weight: 600; }
.barra-fondo { background: var(--fondo-principal); height: 12px; border-radius: 6px; overflow: hidden; }
.barra-progreso { height: 100%; border-radius: 6px; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1), background 0.5s; }
.falta-texto { font-size: 0.9rem; color: var(--texto-secundario); margin-top: 0.8rem; text-align: center; }

.cambiar-foto input { width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6); color: white; text-align: center; }

@media (max-width: 600px) {
  .perfil-stats { flex-direction: column; gap: 1rem; }
  .stat { flex-direction: row; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;}
}
</style>