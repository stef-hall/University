/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package integration;

import domain.Student;
import java.util.Collection;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface StudentClientAPI {

    @POST("/api/students")
    Call<Void> createStudent(@Body Student student);

    @GET("/api/students")
    Call<Collection<Student>> getAllStudents();

    @GET("/api/students/{id}")
    Call<Student> getStudentById(@Path("id") Integer studentId);
}
