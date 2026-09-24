package web;

import dao.JdbiStudentDAO;
import domain.Student;
import io.jooby.Jooby;
import io.jooby.StatusCode;

public class StudentModule extends Jooby {
    

    public StudentModule(JdbiStudentDAO dao) {

        // TODO: GET /api/students -> dao.getAll()
        get("/api/students/", ctx -> dao.getAll());

        // TODO: GET /api/students/{id}
        // Read the path parameter, retrieve the student, return 404 if null.
        get("/api/students/{id}", ctx -> {
            int id = ctx.path("id").intValue();
            Student s = dao.getByID(id);
            if (s == null) {return (StatusCode.NOT_FOUND);}
            return s;
        });

        // TODO: POST /api/students
        // Convert the JSON request body to Student and save it.
        post("/api/students/", ctx -> {
            
            Student s = ctx.body(Student.class);
            dao.save(s);
            return ctx.send(StatusCode.NO_CONTENT);
        });

        // TODO: PUT /api/students/{id}
        // Convert body to Student, set its ID from the path, then update it.
        put("/api/students/{id}", ctx -> {
            int id = ctx.path("id").intValue();
            Student s = ctx.body(Student.class);
            s.setId(id);
            dao.update(s);
            return ctx.send(StatusCode.NO_CONTENT);
        });
        
        // Delete that shit
        delete("/api/students/delete/{id}", ctx -> {
            System.out.println("delete that shi");
            int id = ctx.path("id").intValue();
            Student s = dao.getByID(id);
            dao.delete(s);
            return ctx.send(StatusCode.NO_CONTENT);
        });
    }
}
