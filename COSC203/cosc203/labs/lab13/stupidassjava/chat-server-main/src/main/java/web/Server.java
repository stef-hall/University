package web;

import dao.MessageCollectionsDAO;
import dao.MessageDAO;
import io.jooby.Jooby;
import io.jooby.ServerOptions;
import io.jooby.gson.GsonModule;
import io.jooby.handler.CorsHandler;
import io.jooby.netty.NettyServer;

public class Server extends Jooby {

	private final static MessageDAO dao = new MessageCollectionsDAO();

	public Server(MessageDAO dao) {
		install(new GsonModule(new LocalDateTimeSerialiser().getSerialiser()));
		use(new CorsHandler());
		mount(new ChatModule(dao));
	}

	public static void main(String[] args) {
		System.out.println("\nStarting Server.");
		ServerOptions options = new ServerOptions().setPort(8085);
		runApp(args, new NettyServer(options), () -> new Server(dao));
	}

}
