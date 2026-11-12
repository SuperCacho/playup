<template>
  <div class="home-container">
    <div class="hero glass-panel">
      <h1>Bienvenido a Play Up</h1>
      <p>Tu biblioteca personal de videojuegos, organizada y lista para la acción.</p>
      <router-link to="/biblioteca" class="btn-primary">Ir a la Biblioteca</router-link>
    </div>

    <h2 class="subtitulo">Últimos juegos añadidos</h2>
    <div class="grid-juegos">
      <div v-for="juego in ultimosJuegos" :key="juego.id" class="card-juego glass-panel">
        <img :src="obtenerPortada(juego)" class="portada" alt="Portada" />
        <h3>{{ juego.titulo }}</h3>
        <div class="card-info">
          <span><i class="fa-solid fa-star" style="color: #FBBF24;"></i> {{ juego.puntuacion || 'S/N' }}</span>
          <span><i class="fa-solid fa-clock" style="color: #94A3B8;"></i> {{ juego.duracion_horas || 0 }}h</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/juegos'
const ultimosJuegos = ref([])

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/`)
    // Ordenamos por fecha de creación (los últimos primero) y cortamos los primeros 4
    const juegosOrdenados = res.data.sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en))
    ultimosJuegos.value = juegosOrdenados.slice(0, 4)
  } catch (error) {
    console.error(error)
  }
})

// Función para generar portada si no hay URL
const obtenerPortada = (juego) => {
  if (juego.portada_url) return juego.portada_url
  return `https://placehold.co/600x400/1e293b/38BDF8?text=${encodeURIComponent(juego.titulo)}`
}
</script>

<style scoped>
.hero { padding: 4rem 2rem; text-align: center; border-radius: 16px; margin-bottom: 3rem; }
.hero h1 { font-size: 3rem; color: var(--azul-principal); margin-bottom: 1rem; text-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
.hero p { color: var(--texto-secundario); font-size: 1.2rem; margin-bottom: 2rem; }
.btn-primary { display: inline-block; background: var(--azul-principal); color: black; padding: 0.8rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 800; transition: 0.3s; }
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.4); }
.subtitulo { color: white; margin-bottom: 1.5rem; border-left: 4px solid var(--azul-principal); padding-left: 10px; }
.grid-juegos { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; }
.card-juego { border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
.portada { width: 100%; height: 150px; object-fit: cover; border-bottom: 2px solid var(--azul-principal); }
.card-juego h3 { padding: 1rem 1rem 0.5rem 1rem; margin: 0; color: var(--azul-principal); font-size: 1.1rem; }
.card-info { display: flex; justify-content: space-between; padding: 0 1rem 1rem 1rem; color: var(--texto-secundario); font-weight: 600; }
</style>