import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'
import HelloWorld from '../components/HelloWorld'
import Items from '../views/items'
import Item from '../views/Item'
import AddItem from '../views/AddItem'
import Login from '../views/Login'

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

 /* eslint-disable */ 

export default new Router({
  routes: [
    {
     path: '/',
     name: 'home',
     component: Home
    },
    {
      path: '/hw',
     name: 'helloworld',
     component: HelloWorld
    },
    {
      path: '/about',
     name: 'about',
     component: About
    },
    {
      path: '/items',
     name: 'items',
     component: Items
    },
    {
      path: '/login',
     name: 'login',
     component: Login
    },
    {
      path: "/item/:id",
      name: "item-details",
      component: Item
    },
    {
      path: "/add-item",
      name: "add-item",
      component: AddItem
    },
    {
      path: '*',
     name: 'notfound',
     component: NotFound
    }
  ]
})
