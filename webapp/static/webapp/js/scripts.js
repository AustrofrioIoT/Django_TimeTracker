/*jslint browser: true*/
/*global $, jQuery, alert*/
// Shrink header on scroll and bring in back to top button

function setupScroll() {
    "use strict";
    $(window).scroll(function () {
        if ($(document).scrollTop() > 50) {
            $('header').addClass('header-shrink');
            $('#back-to-top').addClass('visible');
        } else {
            $('header').removeClass('header-shrink');
            $('#back-to-top').removeClass('visible');
        }
    }).scroll();
}

document.addEventListener("touchstart", function() {},false);

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

//Create offcanvas navigation for Bootstrap
function setupOffCanvas() {
    "use strict";
    $(function () {
        $('[data-toggle="offcanvas"]').on('click', function () {
            $('.offcanvas-collapse').toggleClass('open');
        });
    });
    $('.navbar-toggler').click(function () {      // When arrow is clicked
        $('.navbar-toggler').toggleClass('open');
    });
}

//Search
function setupSearch() {
    "use strict";
    $(".search-btn").click(function(){
      $(".search").fadeToggle(200);
    });
    $(".search-close-btn").click(function(){
        $(".search").fadeToggle(200);
    });
    $(document).mouseup(function(e) 
    {
        var container = $(".search");

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            container.hide();
        }
    });
}

//Back To Top
function setupBackToTop() {
    "use strict";
    $('#back-to-top').click(function () {      // When arrow is clicked
        $('body,html').animate({
            scrollTop : 0                       // Scroll to top of body
        }, 500);
    });
}

//Footer Navigation Responsive Dropdowns
function setupFooterNav() {
    "use strict";
    $('.footer-contact-title').click(function () {
        $('ul.footer-contact-list, .footer-contact-title').toggleClass('open');
    });
    $('.footer-product-title').click(function () {
        $('ul.footer-product-list, .footer-product-title').toggleClass('open');
    });
    $('.footer-company-title').click(function () {
        $('ul.footer-company-list, .footer-company-title').toggleClass('open');
    });
    $('.footer-support-title').click(function () {
        $('ul.footer-support-list, .footer-support-title').toggleClass('open');
    });
    $('.footer-resources-title').click(function () {
        $('ul.footer-resources-list, .footer-resources-title').toggleClass('open');
    });
}

//Local Storage for IE10 and lower Alert close
function setupCloseStorage() {
    "use strict";
    function hideIt() {
        localStorage.hidden = 1;
        $(".closeiealert").hide();
    }
    if (localStorage.hidden === "1") {
        hideIt();
    }
    $(".closeiealertbtn").click(hideIt);
}


function setupaddClasses() {
    $("input#ctl00_cphBody_chkRememberMe").addClass("custom-control-input");
    $("span.custom-control.custom-checkbox label").addClass("custom-control-label");
}


function showTime(){
    myDate = new Date();
    hours = myDate.getHours();
    minutes = myDate.getMinutes();
    seconds = myDate.getSeconds();

    if (hours < 10) hours = 0 + hours;

    if (minutes < 10) minutes = "0" + minutes;

    if (seconds < 10) seconds = "0" + seconds;

    $("#HoraActual").text(hours+ ":" +minutes+ ":" +seconds);

    d = myDate.getDate();
    dia = (d < 10) ? '0' + d : d;
    m = myDate.getMonth() + 1;
    mes = (m < 10) ? '0' + m : m;
    anio = myDate.getFullYear();
    $("#FechaActual").text(dia+ "/" +mes+ "/" +anio);

    setTimeout("showTime()", 1000);
}

//Get our functions
function loadWindow(argument) {
    $(window).on('load', function () {
        console.log('entro al windows on');
        setTimeout(function () {
            $(".main").css({visibility:"hidden",opacity:"0"})
        }, 2000);
    });
}
$(document).ready(function () {
    'use strict';
    loadWindow();
    setupScroll();
    setupOffCanvas();
    setupSearch();
    setupBackToTop();
    setupFooterNav();
    setupCloseStorage();
    setupaddClasses();

    showTime();
    // punch();
    // changeState();
    // changeAfk();
    // disabledBtn();
});