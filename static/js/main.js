//   CSRF
// ***********************************/

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            console.log('add csrf');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



function mobileMenuToggle() {
    const navItem = $("#main-navbar > .navbar-item#menu");
    const navbar = $("#main-navbar");
    $.merge(navItem, navbar).toggleClass("responsive");
    $("#main-navbar > .navbar-item#menu-toggle").toggleClass("active");
    $("#main-navbar .dropdown-menu").toggleClass("show");
    $("#page-container").toggleClass("inactive");
    toggleSearch();
}

function closeMobileMenu() {
    if ($("#page-container").hasClass("inactive")) {
        mobileMenuToggle();
    }
}