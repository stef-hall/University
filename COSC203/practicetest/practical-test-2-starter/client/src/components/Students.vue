<template>
  <section>
    <h2>Students</h2>

    <!-- TODO: form with name + major using v-model and @submit.prevent -->

    <!-- TODO: use v-for to display every student -->
    <!-- TODO: add an Edit button that loads a student into the form -->
  </section>
</template>

<script>
import axios from 'axios';

const API = 'http://localhost:8085/api/students';

export default {
  data() {
    return {
      students: [],
      student: {
        id: null,
        name: '',
        major: ''
      }
    };
  },

  mounted() {
    // TODO: retrieve students when component loads
  },

  methods: {
    loadStudents() {
      // TODO: axios GET, then put response.data into this.students
    },

    saveStudent() {
      // TODO:
      // if student.id is null -> POST
      // otherwise -> PUT /{id}
      // then reload students and clear the form
    },

    editStudent(student) {
      // TODO: copy the selected student into this.student
    },

    clearForm() {
      this.student = { id: null, name: '', major: '' };
    }
  }
};
</script>
