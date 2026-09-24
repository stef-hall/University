package dao;

import domain.Student;
import java.util.Collection;

/**
 * A DAO for managing the storage of Student objects.
 */
public interface StudentDAO {

	/**
	 * Adds a student to the DAO.
	 *
	 * @param aStudent The student to add.
	 */
	void save(Student aStudent);

	/**
	 * Deletes a student from the DAO.
	 *
	 * @param aStudent The student to delete.
	 */
	void delete(Student aStudent);

	/**
	 * Returns all students that have been added to the DAO.
	 *
	 * @return The collection of students.
	 */
	Collection<Student> getAll();

	/**
	 * Returns unique collections of majors for students that have been added to
	 * the DAO.
	 *
	 * @return The collection of majors.
	 */
	Collection<String> getMajors();

	/**
	 * Returns the student matching the given ID.
	 *
	 * @param studentID The ID of the student to retrieve.
	 * @return The collection of majors.
	 */
	Student getByID(Integer studentID);

	/**
	 * Returns the students enrolled in a given major.
	 *
	 * @param major The major to filter on.
	 * @return The collection of students in the given major.
	 */
	Collection<Student> filterByMajor(String major);

	/**
	 * Returns a boolean that is true if there is a student matching the given ID.
	 *
	 * @param studentID The ID of the student to search for.
	 * @return Does a student matching the given ID exist or not (boolean).
	 */
	Boolean doesStudentExist(Integer studentID);

}
