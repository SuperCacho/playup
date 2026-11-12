<template>
  <aside class="sidebar glass-panel">
    <div class="logo"><i class="fa-solid fa-gamepad"></i><h2>PLAY UP</h2></div>
    <nav>
      <router-link to="/" class="nav-item"><i class="fa-solid fa-house"></i> Inicio</router-link>
      <router-link to="/dashboard" class="nav-item"><i class="fa-solid fa-chart-pie"></i> Dashboard</router-link>
      <router-link to="/biblioteca" class="nav-item"><i class="fa-solid fa-book"></i> Biblioteca</router-link>
      <router-link to="/ranking" class="nav-item"><i class="fa-solid fa-trophy"></i> Ranking</router-link>
      <router-link to="/perfil" class="nav-item"><i class="fa-solid fa-user"></i> Mi Perfil</router-link>
      
      <!-- OPCIÓN EXCLUSIVA DE ADMIN -->
      <router-link v-if="esAdmin" to="/admin" class="nav-item admin-link">
        <i class="fa-solid fa-shield-halved"></i> Gestión
      </router-link>
    </nav>
    <div class="cerrar-sesion" @click="$emit('logout')"><i class="fa-solid fa-right-from-bracket"></i> Cerrar Sesión</div>
  </aside>
</template>

<script setup>
defineProps({ esAdmin: Boolean })
defineEmits(['logout'])
</script>

<style scoped>
.sidebar { width: 260px; height: 100vh; position: fixed; left: 0; top: 0; display: flex; flex-direction: column; padding: 1.5rem 0; border-right: 1px solid var(--borde); border-radius: 0 16px 16px 0; z-index: 100; background: rgba(30, 41, 59, 0.95); backdrop-filter: blur(10px); }
.logo { display: flex; align-items: center; gap: 10px; padding: 0 1.5rem 2rem 1.5rem; color: var(--azul-principal); font-size: 1.5rem; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
nav { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; overflow-y: auto;}
.nav-item { padding: 1rem 1.5rem; color: var(--texto-secundario); text-decoration: none; display: flex; align-items: center; gap: 15px; font-weight: 600; transition: all 0.3s ease; border-left: 3px solid transparent; }
.nav-item:hover { background: rgba(56, 189, 248, 0.05); color: white; }
.router-link-active { background: rgba(56, 189, 248, 0.15); color: var(--azul-principal); border-left: 3px solid var(--azul-principal); }
.admin-link { color: #FBBF24; } .admin-link:hover { color: #FDE047; } .admin-link.router-link-active { background: rgba(251, 191, 36, 0.15); border-left-color: #FBBF24; color: #FBBF24;}
.cerrar-sesion { padding: 1rem 1.5rem; color: var(--rojo); cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 15px; transition: 0.3s; }
.cerrar-sesion:hover { background: rgba(248, 113, 113, 0.1); }
@media (max-width: 768px) {
  .sidebar { width: 100%; height: 70px; bottom: 0; top: auto; flex-direction: row; padding: 0; border-right: none; border-top: 1px solid var(--borde); border-radius: 0; }
  .logo, .cerrar-sesion { display: none; }
  nav { flex-direction: row; justify-content: space-around; width: 100%; gap: 0; align-items: center; }
  .nav-item { padding: 0.5rem; flex-direction: column; gap: 5px; font-size: 0.7rem; border-left: none; border-top: 3px solid transparent; flex: 1; text-align: center; }
  .router-link-active { border-top: 3px solid var(--azul-principal); border-left: none; }
  .admin-link.router-link-active { border-top: 3px solid #FBBF24; border-left: none; }
}
</style>