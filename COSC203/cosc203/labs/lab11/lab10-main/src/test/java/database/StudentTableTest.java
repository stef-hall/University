package database;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import schemacrawler.schema.Catalog;
import schemacrawler.schema.Schema;
import schemacrawler.schema.Table;
import schemacrawler.tools.utility.SchemaCrawlerUtility;

import us.fatehi.utility.datasource.DatabaseConnectionSource;
import us.fatehi.utility.datasource.DatabaseConnectionSources;
import us.fatehi.utility.datasource.MultiUseUserCredentials;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.contains;
import static org.hamcrest.Matchers.is;
import schemacrawler.schema.Column;
import schemacrawler.schema.TableConstraintColumn;

public class StudentTableTest {

    private static Catalog catalog;
    private static Schema schema;

    @BeforeEach
    public void setUp() {
        DatabaseConnectionSource dataSource = DatabaseConnectionSources
                .newDatabaseConnectionSource(
                        "jdbc:h2:tcp://localhost/~/localhost/students",
                        new MultiUseUserCredentials("sa", "sa")
                );

        catalog = SchemaCrawlerUtility.getCatalog(dataSource, null);
        schema = catalog.lookupSchema("STUDENTS.PUBLIC").get();
    }

    @Test
    public void testTableExists() {
        Optional<Table> studentResult = catalog.lookupTable(schema, "STUDENT");
        assertThat(studentResult.isPresent(), is(true));
    }
    
    @Test
    public void testColumnDefinitions() {
            Optional<Table> studentResult = catalog.lookupTable(schema, "STUDENT");

            Table studentTable = studentResult.get();

            List<Column> columnList = studentTable.getColumns();

            // convert list of columns into a map of columns with the column name as a key
            Map<String, Column> columns = columnList
                            .stream()
                            .collect(Collectors.toMap(column -> column.getName(), column -> column));

            // make sure that there is a column named ID
            assertThat(columns.containsKey("ID"), is(true));

            // make sure that the ID column is an INTEGER
            assertThat(columns.get("ID").getColumnDataType().getFullName(), is("INTEGER"));

            // check that the ID column has a not null constraint
            assertThat(columns.get("ID").isNullable(), is(false));

            // make sure that there is a column named NAME
            assertThat(columns.containsKey("NAME"), is(true));

            // make sure that the NAME column is a VARCHAR
            assertThat(columns.get("NAME").getColumnDataType().getFullName(), is("CHARACTER VARYING"));

            // check that the NAME column has a not null constraint
            assertThat(columns.get("NAME").isNullable(), is(false));		
    }
    
    @Test
    public void testPrimaryKey() {
            Optional<Table> studentResult = catalog.lookupTable(schema, "STUDENT");

            Table studentTable = studentResult.get();

            assertThat(studentTable.hasPrimaryKey(), is(true));

            List<TableConstraintColumn> keyColumns = studentTable.getPrimaryKey().getConstrainedColumns();

            // extract column names from list into a map
            Set<String> keyNames = keyColumns
                            .stream()
                            .map(TableConstraintColumn::getName)
                            .collect(Collectors.toSet());

            assertThat(keyNames, contains("ID"));
    }
}
