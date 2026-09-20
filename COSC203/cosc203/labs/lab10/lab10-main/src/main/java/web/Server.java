package web;

import dao.StudentCollectionsDAO;
import dao.StudentDAO;
import domain.Student;
import io.jooby.Jooby;
import io.jooby.netty.NettyServer;
import io.jooby.ServerOptions;
import io.jooby.StatusCode;
import io.jooby.gson.GsonModule;

public class Server extends Jooby {

	private final static StudentDAO dao = new StudentCollectionsDAO();
        
        public Server() {
            install(new GsonModule());
            mount(new StudentModule(dao));
        }

	public static void main(String[] args) {

		// add some dummy data for testing
		dao.save(new Student(1111, "Boris", "123 Some Street", "555 1234", "PHYS"));
		dao.save(new Student(2222, "Doris", "23 Fake Street", "555 234", "PHYS"));
		dao.save(new Student(3333, "Morris", "634 Another Street", "555 6545", "COSC"));
		dao.save(new Student(4444, "Delores", "3 Random Road", "555 2345", "SENG"));
                
                System.out.println("\nStarting Server.");
                ServerOptions options = new ServerOptions().setPort(8085);
                runApp(args, new NettyServer(options), Server::new);

	}

}
