<template>
  <div class="layout fondo-animado">
    <Sidebar v-if="logueado" @logout="cerrarSesion" :esAdmin="esAdmin" />
    <main :class="['main-content', { 'con-sidebar': logueado }]">
      <div v-if="!logueado" class="login-container">
        <div class="login-box glass-panel">
          <h1 class="logo-login"><i class="fa-solid fa-gamepad"></i> PLAY UP</h1>
          <h2>{{ esRegistro ? 'Crear Cuenta' : 'Iniciar Sesión' }}</h2>
          
          <form @submit.prevent="manejarAuth">
            <div class="input-group">
              <label>Email</label>
              <input v-model="credenciales.email" type="email" required />
            </div>
            
            <div class="input-group">
              <label>Contraseña</label>
              <div class="password-wrapper">
                <input v-model="credenciales.password" :type="mostrarPassword ? 'text' : 'password'" required />
                <i class="fa-solid" :class="mostrarPassword ? 'fa-eye-slash' : 'fa-eye'" @click="mostrarPassword = !mostrarPassword"></i>
              </div>
            </div>

            <div class="checkbox-group">
              <input type="checkbox" id="recordarme" v-model="recordarme" />
              <label for="recordarme">Mantener sesión iniciada</label>
            </div>
            <button type="submit" class="btn-primary" :disabled="cargandoAuth">
              <span v-if="cargandoAuth" class="spinner"></span>
              <span v-else>{{ esRegistro ? 'Registrarse' : 'Entrar' }}</span>
            </button>
          </form>
          <p @click="esRegistro = !esRegistro" class="toggle-auth">{{ esRegistro ? '¿Ya tenés cuenta? Iniciá sesión' : '¿No tenés cuenta? Registrate' }}</p>
        </div>
      </div>
      <router-view v-else></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Sidebar from './components/Sidebar.vue'

const logueado = ref(false)
const esAdmin = ref(false)
const esRegistro = ref(false)
const recordarme = ref(false)
const mostrarPassword = ref(false)
const cargandoAuth = ref(false)
const credenciales = ref({ email: '', password: '' })

const configurarAxios = (token) => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const manejarAuth = async () => {
  cargandoAuth.value = true
  const endpoint = esRegistro.value ? '/api/auth/register' : '/api/auth/login'
  try {
    const res = await axios.post(`http://127.0.0.1:8000${endpoint}`, credenciales.value)
    if (esRegistro.value) {
      alert("¡Registrado con éxito! Ahora podés iniciar sesión.")
      esRegistro.value = false
    } else {
      const storage = recordarme.value ? localStorage : sessionStorage
      storage.setItem('token', res.data.token)
      storage.setItem('rol', res.data.rol)
      configurarAxios(res.data.token)
      logueado.value = true
      esAdmin.value = res.data.rol === 'admin'
    }
  } catch (error) {
    alert(error.response?.data?.detail || "Error en la autenticación")
  } finally {
    cargandoAuth.value = false
  }
}

const cerrarSesion = () => {
  localStorage.removeItem('token'); localStorage.removeItem('rol');
  sessionStorage.removeItem('token'); sessionStorage.removeItem('rol');
  delete axios.defaults.headers.common['Authorization']
  logueado.value = false
  esAdmin.value = false
}

onMounted(() => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token')
  const rol = localStorage.getItem('rol') || sessionStorage.getItem('rol')
  if (token) {
    configurarAxios(token)
    logueado.value = true
    esAdmin.value = rol === 'admin'
  }
})
</script>

<style>
/* ACÁ ESTÁ LA MAGIA QUE SE HABÍA PERDIDO */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
:root { 
  --fondo-principal: #0f172a; 
  --fondo-tarjeta: rgba(30, 41, 59, 0.7); 
  --azul-principal: #38BDF8; 
  --texto-principal: #F8FAFC; 
  --texto-secundario: #94A3B8; 
  --borde: rgba(51, 65, 85, 0.5); 
  --rojo: #F87171; 
  --verde: #4ADE80; 
  --amarillo: #FBBF24; 
}
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }
body { background-color: var(--fondo-principal); color: var(--texto-principal); }
.fondo-animado { min-height: 100vh; background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0f172a, #1e293b); background-size: 400% 400%; animation: gradientBG 15s ease infinite; color: var(--texto-principal); }
@keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.layout { display: flex; }
.main-content { flex: 1; padding: 2rem; transition: margin-left 0.3s; }
.con-sidebar { margin-left: 260px; }
.login-container { display: flex; justify-content: center; align-items: center; height: 100vh; padding: 1rem;}
.glass-panel { background: rgba(30, 41, 59, 0.5); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); border-radius: 16px; padding: 2rem; width: 100%; max-width: 420px; text-align: center; animation: slideUp 0.6s ease-out; }
@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.logo-login { color: var(--azul-principal); font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; text-shadow: 0 0 15px rgba(56, 189, 248, 0.5); }
.login-box h2 { font-size: 1.2rem; color: var(--texto-secundario); margin-bottom: 2rem; font-weight: 400; }
.login-box form { display: flex; flex-direction: column; gap: 1.2rem; }
.input-group { display: flex; flex-direction: column; text-align: left; gap: 0.5rem; }
.input-group label { font-size: 0.85rem; color: var(--texto-secundario); font-weight: 600; }
.input-group > input, .password-wrapper input { padding: 0.8rem; border-radius: 8px; border: 1px solid var(--borde); background: rgba(15, 23, 42, 0.6) !important; color: white !important; outline: none; transition: 0.3s; width: 100%; }
.input-group > input:focus, .password-wrapper input:focus { border-color: var(--azul-principal) !important; box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
.password-wrapper { position: relative; display: flex; align-items: center; }
.password-wrapper i { position: absolute; right: 10px; color: var(--texto-secundario); cursor: pointer; transition: 0.2s; }
.password-wrapper i:hover { color: var(--azul-principal); }
.checkbox-group { display: flex; align-items: center; gap: 0.5rem; justify-content: flex-start; font-size: 0.85rem; color: var(--texto-secundario); }
.checkbox-group input { width: auto; }
.btn-primary { padding: 0.8rem; border-radius: 8px; border: none; background: var(--azul-principal); color: #000; font-weight: 800; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; display: flex; justify-content: center; align-items: center; height: 48px;}
.btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4); }
.btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }
.toggle-auth { color: var(--azul-principal); cursor: pointer; margin-top: 1.5rem; font-size: 0.9rem; transition: 0.3s; }
.toggle-auth:hover { color: white; }
.spinner { width: 20px; height: 20px; border: 3px solid rgba(0, 0, 0, 0.3); border-top-color: #000; border-radius: 50%; animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) { .con-sidebar { margin-left: 0; padding: 4rem 1rem 2rem 1rem; } }
</style>