<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const students = ref([])
const student = ref({})

async function getStudents() {
    const response = await axios.get('/api/students/')
    students.value = response.data
}

async function addStudent() {
    alert(student.value.name);
    axios.post('/api/students/', student.value)
}

onMounted(getStudents)
</script>


<template>
    <h1>Adding</h1>
    
    <div v-for="s in students">
        <p>{{ s }}</p>
    </div>

    <form @submit.prevent="addStudent">
        <div>
            <p>ID</p>
            <input type="number" v-model="student.id" >
        </div>

        <div>
            <p>Name</p>
            <input type="text" v-model="student.name" >
        </div>

        <div>
            <p>Major</p>
            <input type="text" v-model="student.major" >
        </div>

        <button type="submit">Add Jit</button>
        
    </form>
</template>