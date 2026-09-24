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
/* centre the major buttons */
#majors {
	display: block;
	text-align: center;
}

/* add some gaps between the major buttons */
#majors button {
	margin-left: 2pt;
	margin-right: 2pt;
}
</style>
