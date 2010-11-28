 


if (window.innerWidth && window.innerWidth <= 480) { 
    $(document).ready(function(){ 
        $('#header ul').addClass('hide'); 
        $('#header').append('<div class="leftButton" onclick="toggleMenu()">Menu</div>'); 
    });
    function toggleMenu() { 
        $('#header ul').toggleClass('hide'); 
        $('#header .leftButton').toggleClass('pressed'); 
    }
}


$(document).ready(function(){
    loadPage();
});
function loadPage(url) {
    $('body').append('<div id="progress">Loading...</div>');
    if (url == undefined) {
        $('#container').load('home.html #header ul', hijackLinks);
    } else {
        $('#container').load(url + ' #content', hijackLinks);
    }
}

function loadPage(url) {
    $('body').append('<div id="progress">Loading...</div>');
    scrollTo(0,0);
    if (url == undefined) {
        $('#container').load('home.html #header ul', hijackLinks);
    } else {
        $('#container').load(url + ' #content', hijackLinks);
    }
}

function hijackLinks() {
    $('#container a').click(function(e){
        var url = e.target.href;
        if (url.match(/wine-tour.appspot.com/)) {
            e.preventDefault();
            loadPage(url);
        }
    });
    var title = $('h2').html() || 'Hello!';
    $('h1').html(title);
    $('h2').remove();
    $('#progress').remove();
}

var hist = [];
 var startUrl = 'home.html';
 $(document).ready(function(){
     loadPage(startUrl);
 });

function loadPage(url) {
    $('body').append('<div id="progress">Loading...</div>');
    scrollTo(0,0);
    if (url == startUrl) {
        var element = ' #header ul';
    } else {
        var element = ' #content';
    }
   
 $('#container').load(url + element, function(){
    var title = $('h2').html() || 'Hello!';
    $('h1').html(title);
    $('h2').remove();
    $('.leftButton').remove();
    hist.unshift({'url':url, 'title':title});
    if (hist.length > 1) {
        $('#header').append('<div class="leftButton">'+hist[1].title+'</div>');
        $('#header .leftButton').click(function(){
            var thisPage = hist.shift();
            var previousPage = hist.shift();
            loadPage(previousPage.url);
        });
    }
    $('#container a').click(function(e){
        var url = e.target.href;
        if (url.match(/wine-tour.appspot.com/)) {
            e.preventDefault();
            loadPage(url);
        }
    });
    $('#progress').remove();
});
}