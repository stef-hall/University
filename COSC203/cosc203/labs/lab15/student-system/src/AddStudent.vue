<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router'
import { getSelectedStudent } from './selectedStudent';
import { ref, onMounted } from 'vue';
const router = useRouter();
const studentsApiUrl = '/api/students';
const student = ref(new Object());

async function addStudent() {
	try {
        await axios.post(studentsApiUrl, student.value);
        router.push("/");
    } catch(error) {
        console.error(error);
        alert('Error creating student');
    }
}

onMounted(()=>{
	 student.value = getSelectedStudent();
});
</script>

<template>
<section class="add-student">
<h1>Adding student</h1>
            <form action="add-student" method="post" @submit.prevent="addStudent()">
                <label for="id">Student ID</label>
                <div>
                    <input type="number" v-model="student.id" required />
                </div>

                <label for="name">Name</label>
                <div>
                    <input id="name" name="name" type="text" v-model="student.name" required />
                </div>

                <label for="address">Address</label>
                <textarea id="address" name="address" rows="3" v-model="student.address" required></textarea>
                

                <label for="phoneNumber">Phone Number</label>
                <input id="phoneNumber" name="phoneNumber" type="tel" v-model="student.phoneNumber" required>

                <label for="major">Major</label>
                <input id="major" name="major" type="text" v-model="student.major" required>

                <div class="form-actions">
                    <button type="submit">Save Student</button>
                    <a class="nav secondary" href="index.jsp">Cancel</a>
                </div>
            </form>
</section>
</template>

<style scoped>
.add-student {
    max-width: 38rem;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    background: white;
    color: #111827;
}

h1 { margin: 0.35rem 0; }

form { display: grid; gap: 0.5rem; }
label { margin-top: 0.5rem; font-weight: 700; }
input, textarea {
    box-sizing: border-box;
    width: 100%;
    padding: 0.65rem 0.75rem;
    border: 1px solid #9ca3af;
    border-radius: 8px;
    font: inherit;
}
.form-actions { display: flex; gap: 0.75rem; margin-top: 1rem; }
button, .secondary {
    padding: 0.65rem 0.9rem;
    border: 0;
    border-radius: 8px;
    background: #111827;
    color: white;
    cursor: pointer;
    font: inherit;
    font-weight: 700;
    text-decoration: none;
}
.secondary { background: #4b5563; }
</style>
