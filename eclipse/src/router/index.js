import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    component: About,
    // LAZY_LOAD_TREASURE:
    //    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    //    route level code-splitting
    //    this generates a separate chunk (about.[hash].js) for this route
    //    which is lazy-loaded when the route is visited.
    name: 'about'
  }
]

const router = new VueRouter({
  routes
})

export default router
