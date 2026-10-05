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

    private static final ProductDAO dao = new ProductJdbiDAO();

    public Server() {
        install(new GsonModule());
        mount(new ProductModule(dao));
    }

    public static void main(String[] args) {
        System.out.println("\nStarting Server.");

        ServerOptions options = new ServerOptions().setPort(8085);
        runApp(args, new NettyServer(options), Server::new);
    }
}
