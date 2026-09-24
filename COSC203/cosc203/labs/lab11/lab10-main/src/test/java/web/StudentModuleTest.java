/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/JUnit5TestClass.java to edit this template
 */
package web;

import dao.StudentDAO;
import domain.Student;
import io.jooby.Body;
import io.jooby.StatusCode;
import io.jooby.test.MockContext;
import io.jooby.test.MockRouter;
import java.util.Collection;
import java.util.List;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.hamcrest.Matchers.is;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 *
 * @author stefan
 */
public class StudentModuleTest {
    
    private StudentDAO mockDAO;
    private Student student1;
    private Student student2;
    private MockRouter router;
    private MockContext mockCtx;

    @BeforeAll
    public static void setUpClass() { 
    }
    
    @AfterAll
    public static void tearDownClass() {
    }
    
    @BeforeEach
    public void setUp() {
        student1 = new Student(1111, "Student 1", "Address 1", "111 1111", "SENG");
        student2 = new Student(2222, "Student 2", "Address 2", "222 2222", "COSC");

        mockDAO = mock(StudentDAO.class);

        when(mockDAO.getAll()).thenReturn(List.of(student1, student2));
        when(mockDAO.getByID(1111)).thenReturn(student1);

        router = new MockRouter(new StudentModule(mockDAO));
        
        Body mockBody = mock(Body.class);
        mockCtx = new MockContext().setBody(mockBody);

        // stub body to return student1
        when(mockBody.to(Student.class)).thenReturn(student1);
    }
    
    @AfterEach
    public void tearDown() {
    }

    @Test
    public void testGetAllStudents() {
        // trigger the operation
        router.get("/api/students", response -> {

            // check the response code is 200/OK
            assertThat(response.getStatusCode(), is(StatusCode.OK));

            // verify that getAll was called on the mock DAO
            verify(mockDAO).getAll();

            // get the collection of students from the response
            Collection<Student> students = (Collection<Student>) response.value();

            // check that the response has the test students in it
            assertThat(students, containsInAnyOrder(student1, student2));
        });
    }
    
    @Test
    public void testGetByID() {
        router.get("/api/students/1111", response -> {
            assertThat(response.getStatusCode(), is(StatusCode.OK));
            verify(mockDAO).getByID(1111);
            
            Student student = (Student)response.value();
            
            assertEquals(student, student1);
        });
        
        router.get("/api/students/420", response -> {
            assertThat(response.getStatusCode(), is(StatusCode.NOT_FOUND));
            verify(mockDAO).getByID(420);
        });
    }
    
    @Test
    public void testCreateStudent() {
        router.post("/api/students", mockCtx, response -> {
            assertThat(response.getStatusCode(), is(StatusCode.CREATED));
            verify(mockDAO).save(student1);
        });	
    }
    
}
