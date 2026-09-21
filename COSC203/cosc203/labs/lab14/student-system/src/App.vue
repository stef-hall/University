<script setup></script>

<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/view">View Students</router-link>
    <router-link to="/add">Add Student</router-link>
  </nav>

  <main>
    <router-view />
  </main>
</template>

<style scoped>
nav > a {
    padding: 5px;
}
</style>
