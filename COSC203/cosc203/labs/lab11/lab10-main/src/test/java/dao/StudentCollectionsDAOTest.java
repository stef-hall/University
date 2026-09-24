package dao;

public class StudentCollectionsDAOTest extends StudentDAOTest {

	@Override
	protected StudentDAO createDAO() {
		return new StudentCollectionsDAO();
	}
	
}
