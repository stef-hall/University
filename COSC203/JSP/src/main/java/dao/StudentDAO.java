package dao;

import domain.Student;
import java.util.Collection;

/**
 * A DAO for managing the storage of Student objects.
 */
public interface StudentDAO {

	/**
	 * Saves a student.
	 *
	 * @param aStudent The student to add.
	 */
	void save(Student aStudent);

	/**
	 * Deletes a student.
	 *
	 * @param aStudent The student to delete.
	 */
	void delete(Student aStudent);

	/**
	 * Returns all students that have been saved.
	 *
	 * @return The collection of students.
	 */
	Collection<Student> getAll();

	/**
	 * Returns the unique collection of majors for students that have been saved.
	 *
	 * @return The collection of majors.
	 */
	Collection<String> getMajors();

	/**
	 * Returns the student matching the given ID.
	 *
	 * @param studentId The ID of the student to retrieve.
	 * @return The collection of majors.
	 */
	Student getByID(Integer studentId);

	/**
	 * Returns the students enrolled in a given major.
	 *
	 * @param major The major to filter on.
	 * @return The collection of students in the given major.
	 */
	Collection<Student> filterByMajor(String major);

	/**
	 * Does a student that matches the given ID exist?
	 *
	 * @param studentId The student ID to look for.
	 * @return true if the student exists, false if not.
	 */
	Boolean doesStudentExist(Integer studentId);

}
