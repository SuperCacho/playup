import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Biblioteca from '../views/Biblioteca.vue'
import Dashboard from '../views/Dashboard.vue'
import Perfil from '../views/Perfil.vue'
import Ranking from '../views/Ranking.vue'
import Admin from '../views/Admin.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: Home },
        { path: '/dashboard', name: 'dashboard', component: Dashboard },
        { path: '/biblioteca', name: 'biblioteca', component: Biblioteca },
        { path: '/ranking', name: 'ranking', component: Ranking },
        { path: '/perfil', name: 'perfil', component: Perfil },
        { path: '/admin', name: 'admin', component: Admin }
    ]
})
export default router