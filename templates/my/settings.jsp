
<!DOCTYPE html>
<html>
<head>
    <%--<link type="text/css" rel="stylesheet" href="stylesheet.css"/>--%>
    <title>Settings</title>
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
        <h1>Settings</h1>

            <form method="post" action="/changeNick">
                    <h2>Change nick</h2>
                    <input type="text" name="newNick" size="25%" value="" placeholder="New nick">
                    <p><input class="change" type="submit" value="Change"></p>
            </form>
            <hr>
            <form method="post" action="/changeEmail">
                    <h2>Change email</h2>
                    <input type="text" name="newEmail" size="25%" value="" placeholder="New email">
                    <p><input class="change" type="submit" value="Change"></p>
            </form>
             <hr>
            <form method="post" action="/changePass">
                    <h2>Change password</h2>
                    <input type="password" name="newPassword" size="25%" value="" placeholder="New password">
                    <p><input class="change" type="submit" value="Change"></p>
            </form>
            <hr>
            <form method="post" action="/deleteAccount">
                    <h2>Delete account</h2>
                    <input type="password" name="password" size="25%" value="" placeholder="Confirm password">
                    <p><input class="change" type="submit" value="Confirm"></p>
            </form>
            <hr>

                

                
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