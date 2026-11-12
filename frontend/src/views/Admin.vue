<template>
  <div class="admin-container">
    <div class="header-admin">
      <h1 class="titulo-pagina"><i class="fa-solid fa-shield-halved"></i> Panel de Administrador</h1>
      <input v-model="busqueda" @input="cargarUsuarios" type="search" placeholder="Buscar por correo o usuario..." class="buscador" />
    </div>

    <div class="glass-panel admin-card">
      <h2>Gestión de Usuarios</h2>
      
      <!-- SPINNER DE CARGA DE TABLA -->
      <div v-if="cargando" class="vacio" style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
        <span class="spinner" style="width: 30px; height: 30px; border-width: 3px; border-top-color: var(--azul-principal);"></span>
        Cargando usuarios...
      </div>
      
      <div v-else-if="usuarios.length === 0" class="vacio">No se encontraron usuarios.</div>
      
      <table v-else class="tabla-usuarios">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in usuarios" :key="user.id" :class="{ 'fila-inactiva': !user.activo }">
            <td><i class="fa-solid fa-user-circle"></i> {{ user.username }}</td>
            <td class="email-col">{{ user.email || 'Sin correo' }}</td>
            <td>
              <span class="tag-rol" :class="user.rol">{{ user.rol }}</span>
            </td>
            <td>
              <span class="tag-estado" :class="user.activo ? 'activo' : 'inactivo'">
                {{ user.activo ? 'Activo' : 'Desactivado' }}
              </span>
            </td>
            <td>
              <!-- BOTÓN CON SPINNER -->
              <button 
                @click="toggleUsuario(user)" 
                :class="user.activo ? 'btn-desactivar' : 'btn-activar'" 
                :title="user.activo ? 'Desactivar Cuenta' : 'Reactivar Cuenta'"
                :disabled="procesando"
              >
                <span v-if="procesando" class="spinner" style="width: 15px; height: 15px; border-width: 2px; border-top-color: currentColor;"></span>
                <template v-else>
                  <i class="fa-solid" :class="user.activo ? 'fa-user-slash' : 'fa-user-check'"></i>
                  {{ user.activo ? 'Desactivar' : 'Activar' }}
                </template>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const usuarios = ref([])
const cargando = ref(true)
const procesando = ref(false) // <-- Estado para bloquear el botón y mostrar spinner
const busqueda = ref('')
const API_URL = 'http://127.0.0.1:8000/api/auth'

const cargarUsuarios = async () => {
  try {
    cargando.value = true
    const res = await axios.get(`${API_URL}/usuarios`, {
      params: { search: busqueda.value }
    })
    usuarios.value = res.data
  } catch (error) {
    console.error(error)
  } finally {
    cargando.value = false
  }
}

const toggleUsuario = async (user) => {
  const accion = user.activo ? 'desactivar' : 'activar'
  if (!confirm(`¿Estás seguro de ${accion} la cuenta de ${user.username}?`)) return
  
  procesando.value = true // Bloqueamos el botón
  try {
    await axios.patch(`${API_URL}/usuarios/${user.id}/toggle`)
    await cargarUsuarios()
  } catch (error) {
    alert("Error al cambiar el estado del usuario")
  } finally {
    procesando.value = false // Desbloqueamos
  }
}

onMounted(() => { cargarUsuarios() })
</script>

<style scoped>
.titulo-pagina { color: #FBBF24; font-weight: 800; display: flex; align-items: center; gap: 10px;}
.header-admin { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;}
.buscador { width: 350px; padding: 0.75rem; border-radius: 20px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6); color: white; outline: none; transition: 0.3s;}
.buscador:focus { border-color: #FBBF24; box-shadow: 0 0 10px rgba(251, 191, 36, 0.3); }

.admin-card { max-width: 1000px; margin: 0 auto; padding: 2rem; text-align: left; overflow-x: auto; }
h2 { color: white; margin-bottom: 1.5rem; border-bottom: 1px solid var(--borde); padding-bottom: 10px; }

.tabla-usuarios { width: 100%; border-collapse: collapse; min-width: 700px; }
.tabla-usuarios th, .tabla-usuarios td { padding: 1rem; text-align: left; border-bottom: 1px solid var(--borde); color: white; }
.tabla-usuarios th { color: var(--texto-secundario); font-weight: 600; text-transform: uppercase; font-size: 0.85rem; }

.email-col { color: var(--texto-secundario); font-size: 0.9rem; }
.fila-inactiva { opacity: 0.6; }

.tag-rol { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
.tag-rol.admin { background: rgba(251, 191, 36, 0.2); color: #FBBF24; }
.tag-rol.coleccionista { background: rgba(56, 189, 248, 0.2); color: var(--azul-principal); }

.tag-estado { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
.tag-estado.activo { background: rgba(74, 222, 128, 0.2); color: #4ADE80; }
.tag-estado.inactivo { background: rgba(248, 113, 113, 0.2); color: #F87171; }

.btn-desactivar, .btn-activar { 
  padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-weight: bold; 
  transition: 0.3s; border: 1px solid; display: flex; align-items: center; 
  justify-content: center; gap: 8px; min-width: 120px;
}
.btn-desactivar { background: transparent; color: var(--rojo); border-color: var(--rojo); }
.btn-desactivar:hover:not(:disabled) { background: var(--rojo); color: white; }

.btn-activar { background: transparent; color: var(--verde); border-color: var(--verde); }
.btn-activar:hover:not(:disabled) { background: var(--verde); color: black; }

.btn-desactivar:disabled, .btn-activar:disabled { opacity: 0.5; cursor: not-allowed; }

.vacio { text-align: center; color: var(--texto-secundario); padding: 2rem; }

@media (max-width: 768px) {
  .header-admin { flex-direction: column; align-items: stretch; }
  .buscador { width: 100%; }
  .admin-card { padding: 1rem; }
}
</style>