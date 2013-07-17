function initsubpage() {
    console.log('initsubpage');
    $("#tabs").tabs();
    $("a.gallery-link").click(function(e){
        path = $(this).attr('href');
        loadGallery(e, path);
    });
    $("a.gallery-back").click(function(e){
        $("#gallery-info").show();
        $("#gallery-view").hide();
        e.preventDefault();
    });
    $(".local").click(function(e) {
        if (!e.ctrlKey)
            console.log("local link");
            setsubpage(e, $(this).attr("href"));
    });
    jQuery('a.gallery').colorbox({rel:'gallery'});
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
            var headerindex = response.indexOf("__AJAX__");
            if (headerindex != -1) {
                var pageTitle = response.substring(0,headerindex);
                var content = response.substring(headerindex + 9);
                document.title = pageTitle;
                $("#content").html(content);
                initsubpage();
                window.history.pushState({"content":content,"pageTitle":pageTitle},"", path);
                setNavSelected(window.location.pathname);
            }
            else {
                window.location = path;
            }
        }
    });
    e.preventDefault();
}

function loadGallery(e, path) {
    if (!e.ctrlKey) {
        $.ajax({
            url: path, 
            type: 'GET',
            success: function (response) {
                var headerindex = response.indexOf("__AJAX__");
                if (headerindex != -1) {
                    var pageTitle = response.substring(0,headerindex);
                    var content = response.substring(headerindex + 9);
                    document.title = pageTitle;
                    $("#gallery-info").hide();
                    $("#gallery-view").html(content).show();
                    initsubpage();
                    window.history.pushState({"content":content,"pageTitle":pageTitle},"", window.location.pathname);
                    setNavSelected(window.location.pathname);
                }
                else {
                    window.location = path;
                }
            }
        });
        e.preventDefault();
    }
}

window.onpopstate = function(e){
    if(e.state){
        $("content").html = e.state.content;
        document.title = e.state.pageTitle;
    }
};

function setNavSelected(path) {
    var secondSlash = path.substr(1).indexOf('/')
    if (secondSlash > 0)
        path = path.substr(0,secondSlash + 1);
    console.log('path: ' + path);
    $("#nav-global a").attr('id', '');
    $('#nav-global a[href="' + path + '"]').attr('id', 'nav-selected');
}

$(document).ready(function() {
    $("#nav-global a").click(function(e) {
        if (!e.ctrlKey)
            setsubpage(e, $(this).attr("href"));
    });
    setNavSelected(window.location.pathname);
    initsubpage();
});
