<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page import="domain.Student"%>
<%@page import="java.util.Map"%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Update Student</title>
        <link rel="stylesheet" href="css/layout.css">
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <%@include file="WEB-INF/jspf/navigation.jspf"%>
        <main>
            <h1>Update Student</h1>
            <%
                Student student = (Student) session.getAttribute("student");
                Map<String, String> errors = (Map<String, String>) session.getAttribute("validationErrors");
                session.removeAttribute("validationErrors");
            %>
            <% if (student == null) { %>
                <p class="empty-state">Choose a student from the student list before updating their details.</p>
                <a class="nav secondary" href="view-students.jsp">View Students</a>
            <% } else { %>
                <form action="add-student" method="post">
                    <input type="hidden" name="returnPage" value="update-student.jsp">
                    <label for="id">Student ID</label>
                    <div>
                        <input id="id" name="id" type="number" value="<%= student.getId() %>" readonly>
                        <% if (errors != null && errors.containsKey("id")) { %><p class="field-error"><%= errors.get("id") %></p><% } %>
                    </div>

                    <label for="name">Name</label>
                    <div>
                        <input id="name" name="name" type="text" value="<%= student.getName() %>" required aria-describedby="name-error">
                        <% if (errors != null && errors.containsKey("name")) { %><p id="name-error" class="field-error"><%= errors.get("name") %></p><% } %>
                    </div>

                    <label for="address">Address</label>
                    <textarea id="address" name="address" rows="3" required><%= student.getAddress() %></textarea>

                    <label for="phoneNumber">Phone Number</label>
                    <input id="phoneNumber" name="phoneNumber" type="tel" value="<%= student.getPhoneNumber() %>" required>

                    <label for="major">Major</label>
                    <input id="major" name="major" type="text" value="<%= student.getMajor() %>" required>

                    <div class="form-actions">
                        <button type="submit">Update Student</button>
                        <a class="nav secondary" href="view-students.jsp">Cancel</a>
                    </div>
                </form>
            <% } %>
        </main>
    </body>
</html>
