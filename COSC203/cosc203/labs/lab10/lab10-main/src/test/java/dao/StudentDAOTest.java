package dao;

import domain.Student;
import java.util.Collection;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.nullValue;
import static org.hamcrest.MatcherAssert.assertThat;
import org.hamcrest.Matchers;
import static org.hamcrest.Matchers.contains;
import static org.hamcrest.Matchers.hasSize;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public abstract class StudentDAOTest {

	private StudentDAO dao;

	private Student s1;
	private Student s2;
	private Student s3;

	protected abstract StudentDAO createDAO();
	
	@BeforeEach
	public void setUp() {
		// create some dummy data for testing with
		dao = new StudentCollectionsDAO();

		s1 = new Student(1111, "S1_NAME", "S1_ADDRESS", "S1_PHONE", "MAJOR1");
		s2 = new Student(2222, "S2_NAME", "S2_ADDRESS", "S2_PHONE", "MAJOR2");
		s3 = new Student(3333, "S3_NAME", "S3_ADDRESS", "S3_PHONE", "MAJOR3");

		dao.save(s1);
		dao.save(s2);

		// intentionally not saving s3
	}

	@AfterEach
	public void tearDown() {
		dao.delete(s1);
		dao.delete(s2);
		dao.delete(s3);
	}

	@Test
	public void testSave() {
		// make sure that s3 does not yet exist
		assertThat(dao.doesStudentExist(s3.getId()), is(false));

		// save s3
		dao.save(s3);

		// make sure that s3 now exists
		assertThat(dao.doesStudentExist(s3.getId()), is(true));
	}

	@Test
	public void testDelete() {
		// make sure that s1 already exists
		assertThat(dao.doesStudentExist(s1.getId()), is(true));

		// delete s1
		dao.delete(s1);

		// make sure that s1 no longer exists
		assertThat(dao.doesStudentExist(s1.getId()), is(false));
	}

	@Test
	public void testGetAll() {
		Collection<Student> students = dao.getAll();

		assertThat(students, contains(s1, s2));

		// make sure that we haven't swapped/lost any fields
		Student result = students.stream().filter(s -> s.getId().equals(s1.getId())).findFirst().get();
		assertThat(result, Matchers.samePropertyValuesAs(s1));
	}

	@Test
	public void testGetByID() {
		Student result = dao.getByID(s1.getId());

		assertThat(result, is(s1));

		// make sure that we haven't swapped/lost any fields
		assertThat(result, Matchers.samePropertyValuesAs(s1));

		// check that null is returned for a bad ID
		Student bad = dao.getByID(0xBAD);
		assertThat(bad, is(nullValue()));
	}

	@Test
	public void testFilterByMajor() {
		assertThat(dao.filterByMajor(s1.getMajor()), contains(s1));
		assertThat(dao.filterByMajor(s2.getMajor()), contains(s2));
		assertThat(dao.filterByMajor(s3.getMajor()), hasSize(0));

		// make sure that we haven't swapped/lost any fields
		Student result = dao.filterByMajor("MAJOR1").stream().filter(s -> s.getId().equals(s1.getId())).findFirst().get();
		assertThat(result, Matchers.samePropertyValuesAs(s1));
	}

	@Test
	public void testGetMajors() {
		assertThat(dao.getMajors(), contains(s1.getMajor(), s2.getMajor()));
	}

	@Test
	public void testDoesStudentExist() {
		assertThat(dao.doesStudentExist(s1.getId()), is(true));
		assertThat(dao.doesStudentExist(s3.getId()), is(false));
	}

}
