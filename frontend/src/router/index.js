import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'
import HelloWorld from '../components/HelloWorld'

// const routerOptions = [
//   { path: '/', component: 'Home' },
//   { path: '/about', component: 'About' },
//   { path: '*', component: 'NotFound' }
// ]

// const routes = routerOptions.map(route => {
//   return {
//     ...route,
//     component: () => import(`@/components/${route.component}.vue`)
//   }
// })

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/',
     name: 'home',
     component: Home
    },
    {path: '/HelloWorld',
     name: 'helloworld',
     component: HelloWorld
    },
    {path: '/about',
     name: 'about',
     component: About
    },
    {path: '*',
     name: 'notfound',
     component: NotFound
    },

  ]
})
