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
let status_change = false

$(document).ready(function () {
    $('select').formSelect()

    $('.modal').modal({
        onOpenEnd: function () {
            $('#medie_navn').focus();
        },
    })

    $('#fra_afventeraflevering_til_modtaget_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_modtaget_til_klartiltest_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_modtaget_til_tilbagemeldt_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $(".clickable-row").click(function () {
        window.location.href = $(this).data("href");
    })
});
