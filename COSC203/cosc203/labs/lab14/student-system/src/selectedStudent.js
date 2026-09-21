import { ref } from 'vue'

let selectedStudent = new Object();

export function setSelectedStudent(student) {
  selectedStudent = student;
}

export function getSelectedStudent() {
  return selectedStudent;
}