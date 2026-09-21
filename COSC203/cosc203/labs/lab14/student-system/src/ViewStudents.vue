<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { setSelectedStudent } from './selectedStudent';
import { useRouter } from 'vue-router'
const students = ref(new Array());
const studentsApiUrl = '/api/students';
const router = useRouter();

async function getStudents() {
	try {
		let response = await axios.get(studentsApiUrl);
		students.value = response.data;
	} catch (error) {
		console.error(error);
		alert('Error getting students');
	}
}

function update(student) {
    setSelectedStudent(student);
    router.push("/add");
    
}

onMounted( () => {
    getStudents();
});
</script>

<template>
<section class="view-students">
<div class="heading">
    <div>
        <h1>View students</h1>
    </div>
</div>
    <table>
	<thead>
		<tr>
			<th>ID</th>
			<th>Name</th>
			<th>Address</th>
			<th>Phone Number</th>
			<th></th>
		</tr>
	</thead>
	<tbody>
		<tr v-for="student in students">
			<td>{{student.id}}</td>
			<td>{{student.name}}</td>
			<td>{{student.address}}</td>
			<td>{{student.phoneNumber}}</td>
			<td><form @submit.prevent="update(student)"><button>Update</button></form></td>
		</tr>
	</tbody>
    </table>

    <router-link class="nav" to="/">Back to Home</router-link>
</section>
</template>

<style scoped>
.view-students {
    max-width: 58rem;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    background: white;
    color: #111827;
}
.heading { margin-bottom: 1.5rem; }
h1 { margin: 0.35rem 0 0; }
table { width: 100%; border-collapse: collapse; overflow: hidden; border: 1px solid #cbd5e1; border-radius: 10px; background: white; }
th, td { padding: 0.8rem; border-bottom: 1px solid #e5e7eb; text-align: left; }
th { background: #f3f4f6; color: #111827; }
tbody tr:last-child td { border-bottom: 0; }
button { padding: 0.4rem 0.7rem; border: 0; border-radius: 6px; background: #111827; color: white; cursor: pointer; font: inherit; }
.nav { display: inline-block; margin-top: 1.25rem; color: #111827; font-weight: 700; }
</style>
