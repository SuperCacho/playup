<template>
  <div class="ranking-container">
    <h1 class="titulo-pagina">Salón de la Fama</h1>
    <p class="subtitulo">Escalá posiciones demostrando tu dedicación gamer.</p>

    <div class="timeline">
      <div v-for="rango in RANGOS" :key="rango.id" class="rango-card glass-panel" :class="{ 'rango-actual': rango.id === rangoActual.id, 'rango-bloqueado': rango.id > rangoActual.id }">
        <div class="rango-icono" :style="{ backgroundColor: rango.color + '20', color: rango.color }">
          <i class="fa-solid fa-crown" v-if="rango.id === 10"></i>
          <i class="fa-solid fa-medal" v-else-if="rango.id > 6"></i>
          <i class="fa-solid fa-shield-halved" v-else-if="rango.id > 3"></i>
          <i class="fa-solid fa-star" v-else></i>
        </div>
        <div class="rango-info">
          <h3 :style="{ color: rango.color }">{{ rango.nombre }}</h3>
          <p class="requisitos">Requisitos: {{ rango.horas }}h jugadas | {{ rango.juegos }} juegos</p>
        </div>
        <div class="rango-estado">
          <span v-if="rango.id === rangoActual.id" class="tag-actual">ESTÁS ACÁ</span>
          <i v-else-if="rango.id < rangoActual.id" class="fa-solid fa-circle-check icono-check"></i>
          <i v-else class="fa-solid fa-lock icono-lock"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/juegos'
const juegos = ref([])

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

onMounted(async () => {
  try { const res = await axios.get(`${API_URL}/`); juegos.value = res.data } catch (error) { console.error(error) }
})

const totalJuegos = computed(() => juegos.value.length)
const totalHoras = computed(() => juegos.value.reduce((acc, j) => acc + (j.duracion_horas || 0), 0))

const rangoActual = computed(() => {
  let actual = { id: 0, nombre: 'Sin Rango', color: '#94A3B8' }
  for (let r of RANGOS) {
    if (totalHoras.value >= r.horas && totalJuegos.value >= r.juegos) { actual = r }
  }
  return actual
})
</script>

<style scoped>
.ranking-container { max-width: 800px; margin: 0 auto; }
.titulo-pagina { color: var(--azul-principal); font-weight: 800; }
.subtitulo { color: var(--texto-secundario); margin-bottom: 2rem; }
.timeline { display: flex; flex-direction: column; gap: 1rem; }
.rango-card { display: flex; align-items: center; gap: 1.5rem; padding: 1.5rem; border-radius: 12px; transition: 0.3s; border: 1px solid var(--borde); }
.rango-card:hover { transform: translateX(10px); }
.rango-actual { border: 2px solid var(--azul-principal); box-shadow: 0 0 20px rgba(56, 189, 248, 0.3); transform: scale(1.02); }
.rango-actual:hover { transform: scale(1.04); }
.rango-bloqueado { opacity: 0.5; filter: grayscale(0.8); }
.rango-icono { width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 1.8rem; }
.rango-info { flex: 1; }
.rango-info h3 { margin: 0; font-size: 1.3rem; font-weight: 800; }
.requisitos { margin: 5px 0 0 0; color: var(--texto-secundario); font-size: 0.9rem; }
.rango-estado { font-size: 1.5rem; }
.tag-actual { background: var(--azul-principal); color: black; font-size: 0.75rem; font-weight: 800; padding: 0.3rem 0.8rem; border-radius: 20px; letter-spacing: 1px; }
.icono-check { color: var(--verde); }
.icono-lock { color: var(--texto-secundario); font-size: 1.2rem; }
</style>