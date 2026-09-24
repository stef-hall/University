/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/UnitTests/JUnit5TestClass.java to edit this template
 */
package integration;

import dao.StudentDAO;
import domain.Student;
import io.jooby.test.JoobyTest;
import java.io.IOException;
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
import static org.mockito.Mockito.reset;
import static org.mockito.Mockito.when;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import web.Server;

/**
 *
 * @author stefan
 */
@JoobyTest(value = Server.class, port = 0, factoryMethod = "createServer")
public class IntegrationTest {
    
    private StudentClientAPI client;
    private static StudentDAO mockDAO = mock(StudentDAO.class);

    private Student student1;
    private Student student2;
    
    public static Server createServer() {
	return new Server(mockDAO);
    }	
    
    @BeforeEach
    public void setUp(String serverPath) {

        this.client = new Retrofit.Builder()
                .baseUrl(serverPath)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(StudentClientAPI.class);

        student1 = new Student(1111, "Student 1", "Address 1", "111 1111", "SENG");
        student2 = new Student(2222, "Student 2", "Address 2", "222 2222", "COSC");

        reset(mockDAO);

        when(mockDAO.getAll()).thenReturn(List.of(student1, student2));
        when(mockDAO.getByID(1111)).thenReturn(student1);
    }
    
    @AfterEach
    public void tearDown() {
    }

    // TODO add test methods here.
    // The methods must be annotated with annotation @Test. For example:
    //
    @Test
    public void testGetAllStudents() throws IOException {
        Response<Collection<Student>> response = client.getAllStudents().execute();
        assertThat(response.code(), is(200));
        // get the collection of students from the response
        Collection<Student> students = response.body();

        // check that the response has the test students in it
        assertThat(students, containsInAnyOrder(student1, student2));
    }
    
    @Test
    public void getStudentByID() throws IOException {
        Response<Student> response = client.getStudentById(1111).execute();
        Student student = response.body();
        assertEquals(student, student1);
    }
    
    @Test
    public void createNewStudent() throws IOException {
        Response<Void> response = client.createStudent(student1).execute();
        assertThat(response.code(), is(201));
    }

}

