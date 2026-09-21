package dao;

import org.jdbi.v3.core.Jdbi;
import org.jdbi.v3.sqlobject.SqlObjectPlugin;

public class JdbiFactory {
    public static Jdbi create() {
        Jdbi jdbi = Jdbi.create("jdbc:h2:./student-db;AUTO_SERVER=TRUE", "sa", "");
        jdbi.installPlugin(new SqlObjectPlugin());
        return jdbi;
    }
}
