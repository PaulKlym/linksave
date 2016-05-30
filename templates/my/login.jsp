
<!DOCTYPE html>
<html>
<head>
    <%--<link type="text/css" rel="stylesheet" href="stylesheet.css"/>--%>
    <title>Login page</title>
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
        <h1>Login page</h1>

        <table width="25%" align="center">
            <form method="post" action="/login">
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
                    <input type="password" name="password" size="25%" value="" placeholder="Password">
                </td>
                </tr>
                <tr><td>
                    <input type="checkbox" name="remember" />
                    <span class="small">Remember me</span>
                    <input id="login" type="submit" value="Login">
                </td>
                </tr>
            </form>
        </table>

                
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