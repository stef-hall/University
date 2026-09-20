 package dao;

import com.google.common.collect.Multimap;
import com.google.common.collect.TreeMultimap;
import domain.Student;
import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;

/**
 * A DAO that uses collections for storing and managing student objects.
 */
public final class StudentCollectionsDAO implements StudentDAO {

	private static final Map<Integer, Student> students = new TreeMap<>();
	private static final Multimap<String, Student> majors = TreeMultimap.create();

	@Override
	public void save(Student aStudent) {
		Student existingStudent = students.put(aStudent.getId(), aStudent);
		if (existingStudent != null) {
			majors.remove(existingStudent.getMajor(), existingStudent);
		}
		majors.put(aStudent.getMajor(), aStudent);
	}

	@Override
	public void delete(Student aStudent) {
		students.remove(aStudent.getId());
		majors.remove(aStudent.getMajor(), aStudent);
	}

	@Override
	public Collection<Student> getAll() {
		return students.values();
	}

	@Override
	public Collection<String> getMajors() {
		return majors.keySet();
	}

	@Override
	public Student getByID(Integer studentId) {
		return students.get(studentId);
	}

	@Override
	public Collection<Student> filterByMajor(String major) {
		return majors.get(major);
	}

	@Override
	public Boolean doesStudentExist(Integer studentId) {
		return students.containsKey(studentId);
	}

}
