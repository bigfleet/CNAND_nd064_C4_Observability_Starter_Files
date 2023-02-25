$(document).ready(function () {
    var baseurl=window.location.protocol+"//"+window.location.host+window.location.pathname
    // all custom jQuery will go here
    $("#firstbutton").click(function () {
        $.ajax({
            url: baseurl+"/backend/", success: function (result) {
                $("#firstbutton").toggleClass("btn-primary:focus");
                }
        });
    });
    $("#secondbutton").click(function () {
        $.ajax({
            url: baseurl+"/trial/", success: function (result) {
                $("#secondbutton").toggleClass("btn-primary:focus");
            }
        });
    });    
});