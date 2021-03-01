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

function preventBack() { window.history.forward(); }
setTimeout("preventBack()", 0);
window.onunload = function () { null };

let status_change = false

$(document).ready(function () {
    $('select').formSelect()

    $('.modal').modal({
        onOpenEnd: function () {
            $('#wmedie_navn').focus();
            $('#avid_create').focus();
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

    $('#fra_klartiltest_til_begyndtest_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_undertest_til_tilbagemeldt_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_undertest_til_godkendtaftester_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_godkendtaftester_til_parattilgodkendelse_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_parattilgodkendelse_til_godkendt_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_tilbagemeldt_til_afventgenaflevering_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#fra_afventergenaflevering_til_modtaget_dialog').modal(
        {
            dismissible: false,

            onCloseEnd: function () {
                status_change = false
            },
        }
    )

    $('#opret_dialog').modal(
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
