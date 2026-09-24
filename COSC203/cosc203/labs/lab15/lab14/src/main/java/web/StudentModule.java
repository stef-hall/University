package web;

import dao.StudentDAO;
import domain.Student;
import io.jooby.Jooby;
import io.jooby.StatusCode;
import java.util.Collection;

public class StudentModule extends Jooby {
    
    public StudentModule(StudentDAO dao) {

        get("/api/students", ctx -> dao.getAll());

        get("/api/students/{id}", ctx -> {
            Integer id = ctx.path("id").intValue();
            Student student = dao.getByID(id);
            if (student == null) {
                return ctx.send(StatusCode.NOT_FOUND);
            } else {
                return student;
            }
        });
        
        post("/api/students", ctx -> {
            // get student from request body
            Student student = ctx.body().to(Student.class);
            dao.save(student);
            return ctx.send(StatusCode.CREATED);
        });
        
        get("/api/majors", ctx -> dao.getMajors());
        
        get("/api/majors/{major}", ctx -> {
            String major = ctx.path("major").toString();
            Collection<Student> students = dao.filterByMajor(major);
            if (students == null) {
                return ctx.send(StatusCode.NOT_FOUND);
            } else {
                return students;
            }
        });
    }
}