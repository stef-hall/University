package web;

import dao.JdbiStudentDAO;
import domain.Student;
import io.jooby.Jooby;
import io.jooby.StatusCode;

public class StudentModule extends Jooby {

    public StudentModule(JdbiStudentDAO dao) {

        // TODO: GET /api/students -> dao.getAll()

        // TODO: GET /api/students/{id}
        // Read the path parameter, retrieve the student, return 404 if null.

        // TODO: POST /api/students
        // Convert the JSON request body to Student and save it.

        // TODO: PUT /api/students/{id}
        // Convert body to Student, set its ID from the path, then update it.
    }
}
