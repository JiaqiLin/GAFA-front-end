import './assets/main.css'



  
//   // main.ts
//   import './init' // 注意要在createApp 的前面

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
// import router from './router'
import HomePage from '@/pages/HomePage.vue'
import AboutPage from '@/pages/AboutPage.vue'
import { createRouter, createWebHistory } from 'vue-router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



//1.配置路由规则
const routes = [
    {path:"/home", component:HomePage},
    {path:"/about", component:AboutPage}
]
//2.创建路由器
const router = createRouter({
    history: createWebHistory(), //路由工作模式
    routes
})

//3. 加载路由器
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')