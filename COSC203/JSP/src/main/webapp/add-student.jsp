<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@page import="java.util.Map"%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Student</title>
        <link rel="stylesheet" href="css/layout.css">
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <%@include file="WEB-INF/jspf/navigation.jspf"%>
        <main>
            <h1>Add Student</h1>
            <%
                Map<String, String> errors = (Map<String, String>) session.getAttribute("validationErrors");
                session.removeAttribute("validationErrors");
            %>
            <form action="add-student" method="post">
                <label for="id">Student ID</label>
                <div>
                    <input id="id" name="id" type="number" min="1" required aria-describedby="id-error">
                    <% if (errors != null && errors.containsKey("id")) { %><p id="id-error" class="field-error"><%= errors.get("id") %></p><% } %>
                </div>

                <label for="name">Name</label>
                <div>
                    <input id="name" name="name" type="text" required aria-describedby="name-error">
                    <% if (errors != null && errors.containsKey("name")) { %><p id="name-error" class="field-error"><%= errors.get("name") %></p><% } %>
                </div>

                <label for="address">Address</label>
                <textarea id="address" name="address" rows="3" required></textarea>

                <label for="phoneNumber">Phone Number</label>
                <input id="phoneNumber" name="phoneNumber" type="tel" required>

                <label for="major">Major</label>
                <input id="major" name="major" type="text" required>

                <div class="form-actions">
                    <button type="submit">Save Student</button>
                    <a class="nav secondary" href="index.jsp">Cancel</a>
                </div>
            </form>
        </main>
    </body>
</html>
