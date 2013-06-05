/*
function setsubpage(e, path) {
    if (path==null){
        path = '';
    }
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    }
    else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var headerindex = xmlhttp.responseText.indexOf("__AJAX__");
            if (headerindex != -1) {
                var pageTitle = xmlhttp.responseText.substring(0,headerindex);
                var content = xmlhttp.responseText.substring(headerindex + 9);
                document.title = pageTitle;
                $("#content").html(content);
                window.history.pushState({"content":content,"pageTitle":pageTitle},"", path);
            }
            else {
                window.location = path
            }
        }
    }
    xmlhttp.open("GET", path, true);
    xmlhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xmlhttp.send();
    e.preventDefault();
}
*/
function setsubpage(e, path) {
    if (path==null){
        path = '';
    }
    $.ajax({
        url: path,
        type: "GET",
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function (response) {
            var headerindex = response.indexOf("__AJAX__");
            if (headerindex != -1) {
                var pageTitle = response.substring(0,headerindex);
                var content = response.substring(headerindex + 9);
                document.title = pageTitle;
                $("#content").html(content);
                window.history.pushState({"content":content,"pageTitle":pageTitle},"", path);
            }
            else {
                window.location = path;
            }
        }
    });
    e.preventDefault();
}
window.onpopstate = function(e){
    console.log('popstate')
    if(e.state){
        $("content").html = e.state.content;
        document.title = e.state.pageTitle;
    }
};
$(document).ready(function() {
    $("#nav-global a").click(function(e) {
        if (!e.ctrlKey)
            setsubpage(e, $(this).attr("href"));
    });
});
