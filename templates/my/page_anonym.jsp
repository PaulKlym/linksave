
<!DOCTYPE html>
<html>
<head>
    <%--<link type="text/css" rel="stylesheet" href="stylesheet.css"/>--%>
    <title>My Page</title>
        <style>
            <%@include file="/stylesheet.css" %>
        </style>
</head>
<body>

<div class="dark">
    <div id="header">
        <a class="head" href="/index"><img src="img/l.png" id="logo" align="center" /></a>
        <a class="head" href="/page">MyPage</a>
        <a class="head" href="/settings">Settings</a>
        <a class="head" href="/contacts">Contacts</a>
        <a class="head" href="/logout">Log<% if (request.getSession().getAttribute("user") != null) out.print("Out"); else out.print("In"); %></a>
    </div>
</div>
<div class="light">
    <div id="body">
        <h1>Please, login or register to see your links</h1>
                

                
            </div>


    </div>
</div>
<div class="dark_foot">
    <div id="footer">
        2014
    </div>
</div>

</body>
</html>