/**
 * Created by milenkotomic on 14-05-15.
 */
function validateForms() {
    var submitButton = $("#submitButton");
    submitButton.attr('disabled', 'disabled');
    var send = true;
    $("form#formID :input")
        .not(':hidden, :button, #id_exhibitor, #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time').
        each(function () {
            var val = $(this).val().trim();
            if (val == "") {
                send = false;
                $(this).prev().children('div').html("* Este campo es obligatorio.");
            }
            else{
                $(this).prev().children('div').html("");
            }
        });

    $("form#formID #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time")
        .each(function(){
            var val = $(this).val().trim();
            if (val == "") {
                send = false;
                $(this).next().html("* Este campo es obligatorio.");
            }
            else{
                $(this).next().html("");
            }
        });

    //if ($("#id_start_circulation").val().trim() == ""){
    //    $("#id_start_circulation").next().html("* Este campo es obligatorio.");
    //    send = false;
    //}
    //else{
    //    if ($("#id_start_circulation_time").val().trim() == ""){
    //        $("#id_start_circulation_time").next().html("* Este campo es obligatorio.");
    //        send = false;
    //    }
    //    else{
    //        $("#id_start_circulation_time").parent().parent().prev().children('div').html("");
    //    }
    //}
    //
    //if ($("#id_end_circulation").val().trim() == ""){
    //    $("#id_end_circulation").parent().parent().prev().children('div').html("* Ambos campos son obligatorios.");
    //    send = false;
    //}
    //else{
    //    if ($("#id_end_circulation_time").val().trim() == ""){
    //        $("#id_end_circulation_time").parent().parent().prev().children('div').html("* Ambos campos son obligatorios.");
    //        send = false;
    //    }
    //    else{
    //        $("#id_end_circulation_time").parent().parent().prev().children('div').html("");
    //    }
    //}

    if (send)
        $("#processing").show();
    else
        submitButton.removeAttr('disabled');

    return send;
}