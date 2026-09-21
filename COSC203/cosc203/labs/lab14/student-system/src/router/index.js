import { createRouter, createWebHistory } from 'vue-router'

// import components
import Home from '@/Home.vue'
import AddStudent from '@/AddStudent.vue'
import ViewStudents from '@/ViewStudents.vue'

const router = createRouter({
    history: createWebHistory(),

    routes: [
        { path: '/', component: Home },
        { path: '/view', component: ViewStudents },
        { path: '/add', component: AddStudent }
    ]
})

export default router