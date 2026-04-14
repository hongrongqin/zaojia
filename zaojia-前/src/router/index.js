import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        redirect: '/evaluation',
        children: [
            {
                path: 'evaluation',
                name: 'Evaluation',
                component: () => import('../views/evaluation/index.vue')
            },
            {
                path: 'standard',
                name: 'Standard',
                component: () => import('../views/standard/index.vue')
            },
            {
                path: 'maintenance',
                name: 'Maintenance',
                component: () => import('../views/maintenance/index.vue')
            },
            {
                path: 'center',
                name: 'center',
                component: () => import('../views/center/index.vue')
            }
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
