<script>
import Students from './components/Students.vue';
export default { components: { Students } };
</script>

<template>
    <nav>
        <router-link to="/view">View Students</router-link>
        <router-link to="/add">Add Student</router-link>
        <router-link to="/delete">Delete Student</router-link>
    </nav>

    <router-view />
</template>