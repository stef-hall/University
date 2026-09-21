package dao;

import domain.Student;
import java.util.List;
import org.jdbi.v3.sqlobject.config.RegisterBeanMapper;
import org.jdbi.v3.sqlobject.customizer.Bind;
import org.jdbi.v3.sqlobject.customizer.BindBean;
import org.jdbi.v3.sqlobject.statement.SqlQuery;
import org.jdbi.v3.sqlobject.statement.SqlUpdate;

@RegisterBeanMapper(Student.class)
public interface JdbiStudentDAO {

    // TODO: SELECT every student
    List<Student> getAll();

    // TODO: SELECT one student using :id
    Student getById(@Bind("id") Integer id);

    // TODO: INSERT a student using @BindBean
    void save(@BindBean Student student);

    // TODO: UPDATE name and major WHERE id matches
    void update(@BindBean Student student);
}
