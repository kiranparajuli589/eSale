import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/dashboard'
    },
    {
        path: '/dashboard',
        name: 'home',
        component: () =>
            import("../views/DashboardComponent")
    },
    {
        path: '/login',
        name: 'login',
        component: () =>
            import("../views/LoginComponent")
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router
