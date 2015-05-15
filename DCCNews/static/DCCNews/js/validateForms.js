/**
 * Created by milenkotomic on 14-05-15.
 */
function validateForms() {
    var submitButton = $("#submitButton");
    submitButton.attr('disabled', 'disabled');
    var send = true;
    $("form#formID :input").not(':hidden, :button, #id_exhibitor').each(function () {
        var val = $(this).val().trim();
        if (val == "") {
            send = false;
            $(this).prev().children('div').html("* Este campo es obligatorio.");
        }
        else{
            $(this).prev().children('div').html("");
        }
    });
    if (send)
        $("#processing").show();
    else
        submitButton.removeAttr('disabled');

    return send;
}