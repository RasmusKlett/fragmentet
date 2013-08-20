var contentdiv = null;
var animationList = [];
var animating = 0;

function popAnimation() {
    animating--;
    if (animationList.length != 0) {
        a = animationList.shift();
        a();
    }
}

function pushAnimation(a) {
    if (animationList.length != 0 || animating > 0) {
        animating++;
        animationList.push(a);
    }
    else {
        animating++;
        a();
    }
}

function initsubpage() {
    //Find any tabs to intercept
    $("#tabs").tabs();
    //Find gallery links to intercept
    $("a.gallery-link").click(function(e){
        path = $(this).attr('href');
        loadGallery(e, path);
    });
    $("a.gallery-back").click(function(e){
        $("#gallery-info").show();
        $("#gallery-view").hide();
        e.preventDefault();
    });
    //Intercept local links
    $(".local").click(function(e) {
        if (!e.ctrlKey)
            setsubpage(e, $(this).attr("href"));
    });
    jQuery('a.gallery').colorbox({rel:'gallery'});
}

function handleAJAXResponse(response, path) {
    var setContent = function (){
        //console.log('AJAX')
        var headerindex = response.indexOf("__AJAX__");
        if (headerindex != -1) {
            var pageTitle = response.substring(0,headerindex);
            var content = response.substring(headerindex + 9);
            document.title = pageTitle;
            contentdiv.html(content);
            initsubpage();
            window.history.pushState({"myContent":content,"pageTitle":pageTitle, "path":path},"", path);
            setNavSelected(window.location.pathname);
        }
        else {
            window.location = path;
        }
        popAnimation();
    };
    pushAnimation(setContent);

    //Display content
    pushAnimation(function() {
        //console.log('fadeIn');
        contentdiv.animate({opacity:1},"fast", popAnimation);
        $("#loading-image").hide();
    });
}


function setsubpage(e, path) {
    if (path==null){
        path = '';
    }
    var animFunc = function(){
        $("#loading-image").show();
        contentdiv.animate({opacity:0},"fast", popAnimation);
    };
    pushAnimation(animFunc);
    $.ajax({
        url: path,
        type: "GET",
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function(response) {handleAJAXResponse(response, path);},
        error: function(jqXHR, textStatus, error) {
            console.log(jqXHR)
            console.log(textStatus)
            console.log(error)
            window.location = path;
        }
    });
    e.preventDefault();
}

function loadGallery(e, path) {
    if (!e.ctrlKey && $("#tab-gallery").length > 0) {
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
                    window.history.pushState({"myContent":content,"pageTitle":pageTitle, "path":path},"", window.location.pathname);
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
    console.log('contentdiv.length: ')
    console.log(contentdiv.length)
    console.log(e.state)
    if(e.state && contentdiv.length > 0){
        console.log('onpopstate: contentdiv exists')
        contentdiv.html(e.state.myContent)
        document.title = e.state.pageTitle;
    }
    else 
        window.location = e.state.path;
};

function setNavSelected(path) {
    var secondSlash = path.substr(1).indexOf('/')
    if (secondSlash > 0)
        path = path.substr(0,secondSlash + 1);
    //console.log('path: ' + path);
    $("#nav-global a").attr('id', '');
    $('#nav-global a[href="' + path + '"]').attr('id', 'nav-selected');
}

$(document).ready(function() {
    contentdiv = $("#content");
    $("#nav-global a").click(function(e) {
        if (!e.ctrlKey)
            setsubpage(e, $(this).attr("href"));
    });
    setNavSelected(window.location.pathname);
    initsubpage();
});
