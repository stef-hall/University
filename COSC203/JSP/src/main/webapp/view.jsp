<%-- 
    Document   : view
    Created on : 17 Aug 2026, 10:44:16 am
    Author     : stefa
--%>

<%@page import="java.util.ArrayList"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <a href="index.jsp">GoBack</a>
        
        <% ArrayList games = (ArrayList) session.getAttribute("games"); 
            if (games != null) {
           for (Object game : games) {%>
                <li><%= game%><li>
           <% } }%>
        
        
        
    </body>
</html>
