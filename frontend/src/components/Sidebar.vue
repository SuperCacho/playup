<template>
  <!-- Botón Hamburguesa (Solo visible en móvil) -->
  <button class="hamburger-btn" @click="menuAbierto = !menuAbierto">
    <i class="fa-solid" :class="menuAbierto ? 'fa-xmark' : 'fa-bars'"></i>
  </button>

  <!-- Fondo oscuro para cerrar el menú al tocar afuera (Solo móvil) -->
  <div v-if="menuAbierto" class="overlay" @click="menuAbierto = false"></div>

  <aside class="sidebar glass-panel" :class="{ 'abierto': menuAbierto }">
    <div class="logo"><i class="fa-solid fa-gamepad"></i><h2>PLAY UP</h2></div>
    <nav>
      <router-link to="/" class="nav-item" @click="menuAbierto = false"><i class="fa-solid fa-house"></i> Inicio</router-link>
      <router-link to="/dashboard" class="nav-item" @click="menuAbierto = false"><i class="fa-solid fa-chart-pie"></i> Dashboard</router-link>
      <router-link to="/biblioteca" class="nav-item" @click="menuAbierto = false"><i class="fa-solid fa-book"></i> Biblioteca</router-link>
      <router-link to="/ranking" class="nav-item" @click="menuAbierto = false"><i class="fa-solid fa-trophy"></i> Ranking</router-link>
      <router-link to="/perfil" class="nav-item" @click="menuAbierto = false"><i class="fa-solid fa-user"></i> Mi Perfil</router-link>
      <router-link v-if="esAdmin" to="/admin" class="nav-item admin-link" @click="menuAbierto = false"><i class="fa-solid fa-shield-halved"></i> Gestión</router-link>
    </nav>
    <div class="cerrar-sesion" @click="$emit('logout'); menuAbierto = false">
      <i class="fa-solid fa-right-from-bracket"></i> Cerrar Sesión
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ esAdmin: Boolean })
defineEmits(['logout'])
const menuAbierto = ref(false)
</script>

<style scoped>
/* BOTÓN HAMBURGUESA */
.hamburger-btn {
  display: none;
  position: fixed; top: 15px; left: 15px; z-index: 1000;
  background: #1e293b; color: var(--azul-principal);
  border: 1px solid var(--borde); border-radius: 8px;
  font-size: 1.5rem; padding: 8px 12px; cursor: pointer;
}

.overlay {
  display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.6); z-index: 998; backdrop-filter: blur(2px);
}

/* MENÚ ESCRITORIO */
.sidebar { 
  width: 260px; height: 100vh; position: fixed; left: 0; top: 0; 
  display: flex; flex-direction: column; padding: 1.5rem 0; 
  border-right: 1px solid var(--borde); border-radius: 0 16px 16px 0; 
  z-index: 999; background: rgba(30, 41, 59, 0.95); backdrop-filter: blur(10px);
  transition: transform 0.3s ease-in-out;
}
.logo { display: flex; align-items: center; gap: 10px; padding: 0 1.5rem 2rem 1.5rem; color: var(--azul-principal); font-size: 1.5rem; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
nav { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; overflow-y: auto;}
.nav-item { padding: 1rem 1.5rem; color: var(--texto-secundario); text-decoration: none; display: flex; align-items: center; gap: 15px; font-weight: 600; transition: all 0.3s ease; border-left: 3px solid transparent; }
.nav-item:hover { background: rgba(56, 189, 248, 0.05); color: white; }
.router-link-active { background: rgba(56, 189, 248, 0.15); color: var(--azul-principal); border-left: 3px solid var(--azul-principal); }
.admin-link { color: #FBBF24; } .admin-link:hover { color: #FDE047; } .admin-link.router-link-active { background: rgba(251, 191, 36, 0.15); border-left-color: #FBBF24; color: #FBBF24;}
.cerrar-sesion { padding: 1rem 1.5rem; color: var(--rojo); cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 15px; transition: 0.3s; }
.cerrar-sesion:hover { background: rgba(248, 113, 113, 0.1); }

/* MODO MÓVIL */
@media (max-width: 768px) {
  .hamburger-btn { display: block; }
  .overlay { display: block; }
  .sidebar { transform: translateX(-100%); width: 280px; }
  .sidebar.abierto { transform: translateX(0); }
}
</style>