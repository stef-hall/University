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
    @SqlQuery("SELECT * FROM student")
    @RegisterBeanMapper(Student.class)
    List<Student> getAll();

    // TODO: SELECT one student using :id
    @SqlQuery("SELECT * FROM student WHERE id=:id")
    @RegisterBeanMapper(Student.class)
    Student getByID(@Bind("id") int id);

    // TODO: INSERT a student using @BindBean
    @SqlUpdate("INSERT INTO student(name,major) VALUES(:name,:major)")
    void save(@BindBean Student student);

    // TODO: UPDATE name and major WHERE id matches
    @SqlUpdate("UPDATE student SET name=:name, major=:major WHERE id=:id")
    void update(@BindBean Student student);
    
    // TODO: DELETE where uh fucking uh can i get a bigmac?
    @SqlUpdate("DELETE FROM student WHERE id = :id")
    void delete(@BindBean Student student);
    
}
