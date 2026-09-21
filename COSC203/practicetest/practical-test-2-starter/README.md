# Practical Test 2 Practice Starter

Goal: implement a tiny Student system using the same pipeline as Labs 9–14:

Vue -> Axios -> Jooby REST -> Jdbi -> H2 database

## Your tasks
1. Complete the Jdbi DAO methods in `server/src/main/java/dao/JdbiStudentDAO.java`.
2. Complete the Jooby routes in `server/src/main/java/web/StudentModule.java`.
3. Run the server on port 8085.
4. Complete the Vue component in `client/src/components/Students.vue` so it:
   - retrieves all students
   - displays them
   - adds a student
   - selects a student for editing
   - updates a student
5. Run the Vue client with `npm install` then `npm run dev`.

This starter intentionally contains TODOs rather than the completed solution.
