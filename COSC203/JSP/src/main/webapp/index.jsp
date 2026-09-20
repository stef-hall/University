<%-- 
    Document   : index
    Created on : 17 Aug 2026, 10:42:14 am
    Author     : stefa
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <h1>Hello World!</h1>
        <form action="add" method="POST">
            <input name="game">
            <button type="submit" >Add Game</button>
        </form>
        <a href="view.jsp">View ></a>
    </body>
</html>
