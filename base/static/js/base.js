//document.addEventListener('DOMContentLoaded', function () {
//    var Modalelem = document.getElementById("opret_medie");
//    var instance = M.Modal.init(Modalelem);
//});

//document.addEventListener('DOMContentLoaded', function () {
//var Modalelem = document.getElementById("hjaelp");
//    var instance = M.Modal.init(Modalelem);
//});

//document.addEventListener('DOMContentLoaded', function () {
//    var elems = document.querySelectorAll('select');
//    var instances = M.FormSelect.init(elems, options);
//});

$(document).ready(function () {
    $('select').formSelect();
    $('.modal').modal({
        onOpenEnd: function () {
            $('#medie_navn').focus();
        }
    });
    $(".clickable-row").click(function () {
        window.location.href = $(this).data("href");
    });
});
