<!DOCTYPE html>
<html>
<head>
    <%--<link type="text/css" rel="stylesheet" href="stylesheet.css" />--%>
    <title>Register</title>
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
        <table width="25%">
            <form method="post" action="/register">
                <tr>    
                    <td>
                        <h1>Welcome</h1>
                    </td>

                </tr>   
                <tr><td>
                <input type="text" name="email" size="25%" value="" placeholder="Email">
                </td>
            </tr>
             <tr><td>
                <input type="text" name="nick" size="25%" value="" placeholder="Nick">
                </td>
            </tr>
            <tr><td>
                <input type="password" name="password" size="25%" value="" placeholder="Password">
            </td>
            </tr>
            <tr><td>
                    <input id="login" type="submit" value="Register">
                </td>
            </tr>
            <tr><td>
                    <span class="small" style="float:right;"><a href="/index_fog">Forgot</a> / <a href="/index">Login</a>
                    </span>
                
            </td>
        </tr>
            </form>
        </table>
    </div>
</div>

<div class="dark_foot">
    <div id="footer">
        2014
    </div>
</div>

</body>
</html>