<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const students = ref([])
const student = ref({})

async function getStudents() {
    const response = await axios.get('/api/students/')
    students.value = response.data
}

async function deleteStudent(id) {
    alert(id);
    axios.delete('/api/students/delete/' + id, student.value);
}

onMounted(getStudents)
</script>


<template>
    <h1>Deleting</h1>
        <div v-for="s in students">
            <p>{{ s.id }}</p>
            <p>{{ s.name }}</p>
            <button @click="deleteStudent(s.id)">Delete {{s.name}} </button>
        </div>
</template>