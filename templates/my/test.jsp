<html>
<head>
<title>Ajax example</title>
<script type="text/javascript">
function ajaxAsyncRequest(reqURL)
{
    //Creating a new XMLHttpRequest object
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest(); //for IE7+, Firefox, Chrome, Opera, Safari
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP"); //for IE6, IE5
    }
    //Create a asynchronous GET request
    xmlhttp.open("GET", reqURL, true);
     
    //When readyState is 4 then get the server output
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200)
            {
                document.getElementById("message").innerHTML = xmlhttp.responseText;
                //alert(xmlhttp.responseText);
            }
            else
            {
                alert('Something is wrong !!');
            }
        }
    };
     
    xmlhttp.send(null);
}
</script>
</head>
<body>

	<input type="button" value="Show Server Time" onclick='ajaxAsyncRequest("/test")'/>
	Here is going to be a result data: <span id="message">"here"</span>
</body>
</html>