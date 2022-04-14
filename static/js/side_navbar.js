
(function($) {
    "use strict";
    $("body").removeClass("sb-sidenav-toggled");
    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            console.log(path);
            //var patharr = path.split("/");
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });


    $("#toggle-todays-app").click((e)=>{
        e.preventDefault();
        $("#dataTable-all-app").css("display", "none");
        $("#dataTable-today-app").slideDown("slow","swing");
    });

    $("#toggle-all-app").click((e)=>{
        e.preventDefault();
        $("#dataTable-today-app").css("display", "none");
        $("#dataTable-all-app").slideDown("slow","swing");
    });

    $("#today-app-search").on("keyup", function(e){ 
        e.preventDefault();
        var value = $(this).val().toLowerCase();

        $("#today-app-data tr").filter(function(){
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    $("#all-app-search").on("keyup", function(e){ 
        e.preventDefault();
        var value = $(this).val().toLowerCase();

        $("#all-app-data tr").filter(function(){
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
    
})(jQuery);
