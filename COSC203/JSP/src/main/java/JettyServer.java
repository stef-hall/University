
import java.nio.file.Path;
import org.eclipse.jetty.ee8.webapp.Configuration;
import org.eclipse.jetty.ee8.webapp.Configurations;
import org.eclipse.jetty.ee8.webapp.WebAppContext;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;



public class JettyServer {

	private static final Integer PORT = 8084;
	private static final String CONTEXT_PATH = "/students-system";

	public static void main(String[] args) throws Exception {

		Server server = new Server();
		ServerConnector connector = new ServerConnector(server);

		connector.setPort(PORT);
		connector.setHost("localhost");

		WebAppContext context = new WebAppContext();

                context.setConfigurations(Configurations.getServerDefault(server).toArray(new Configuration[0]));
                
                context.setBaseResource(context.getResourceFactory().newResource(Path.of("build/deploy")));
		context.setContextPath(CONTEXT_PATH);
		context.setParentLoaderPriority(true);
		server.addConnector(connector);
		server.setHandler(context);

		server.start();

		System.out.println("\nStudents System server ready on:\n\n" + server.getURI());

		server.join();
	}

}