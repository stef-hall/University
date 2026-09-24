import { createRouter, createWebHistory } from 'vue-router'

import ViewStudents from '../View.vue'
import AddStudent from '../Add.vue'
import DeleteStudent from '../Delete.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/view', component: ViewStudents },
        { path: '/add', component: AddStudent },
        { path: '/delete', component: DeleteStudent }
    ]
})

export default router