function initsubpage() {
    $("#tabs").tabs();
    $(".local").click(function(e) {
        if (!e.ctrlKey)
            console.log("local link");
            setsubpage(e, $(this).attr("href"));
    });
}

function setsubpage(e, path) {
    if (path==null){
        path = '';
    }
    $.ajax({
        url: path,
        type: "GET",
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function (response) {
            $("#nav-global a").attr('id', '');
            e.target.setAttribute('id', 'nav-selected');
            var headerindex = response.indexOf("__AJAX__");
            if (headerindex != -1) {
                var pageTitle = response.substring(0,headerindex);
                var content = response.substring(headerindex + 9);
                document.title = pageTitle;
                $("#content").html(content);
                initsubpage();
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
    if(e.state){
        $("content").html = e.state.content;
        document.title = e.state.pageTitle;
    }
};

function getParentPath(path) {
    var secondSlash = path.substr(1).indexOf('/')
    if (secondSlash > 0)
        path = path.substr(0,secondSlash + 1);
    console.log('path: ' + path);
    return path.toLowerCase()
}

$(document).ready(function() {
    $("#nav-global a").click(function(e) {
        if (!e.ctrlKey)
            setsubpage(e, $(this).attr("href"));
    });
    var parentPath = getParentPath(window.location.pathname);
    $('#nav-global a[href="' + parentPath + '"]').attr('id', 'nav-selected');
    initsubpage();
});
