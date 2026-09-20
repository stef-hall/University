<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page import="dao.StudentCollectionsDAO"%>
<%@page import="dao.StudentDAO"%>
<%@page import="domain.Student"%>
<%@page import="java.util.Collection"%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Students</title>
        <link rel="stylesheet" href="css/layout.css">
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <%@include file="WEB-INF/jspf/navigation.jspf"%>
        <main>
            <h1>Students</h1>
            <%
                StudentDAO dao = new StudentCollectionsDAO();
                String selectedMajor = request.getParameter("major");
                Collection<Student> students;

                if (selectedMajor == null || selectedMajor.equals("All")) {
                    students = dao.getAll();
                } else {
                    students = dao.filterByMajor(selectedMajor);
                }
            %>
            <nav class="filters" aria-label="Filter students by major">
                <a class="filter <%= selectedMajor == null || selectedMajor.equals("All") ? "selected" : "" %>" href="view-students.jsp?major=All">All</a>
                <% for (String major : dao.getMajors()) { %>
                    <a class="filter <%= major.equals(selectedMajor) ? "selected" : "" %>" href="view-students.jsp?major=<%= major %>"><%= major %></a>
                <% } %>
            </nav>

            <% if (students.isEmpty()) { %>
                <p class="empty-state">No students match this filter yet.</p>
            <% } else { %>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Address</th>
                            <th>Phone Number</th>
                            <th>Major</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <% for (Student student : students) { %>
                            <tr>
                                <td><%= student.getId() %></td>
                                <td><%= student.getName() %></td>
                                <td><%= student.getAddress() %></td>
                                <td><%= student.getPhoneNumber() %></td>
                                <td><%= student.getMajor() %></td>
                                <td>
                                    <form action="view-student" method="post">
                                        <input type="hidden" name="id" value="<%= student.getId() %>">
                                        <button type="submit">Update</button>
                                    </form>
                                </td>
                            </tr>
                        <% } %>
                    </tbody>
                </table>
            <% } %>
            <a class="nav secondary" href="index.jsp">Back to Menu</a>
        </main>
    </body>
</html>
