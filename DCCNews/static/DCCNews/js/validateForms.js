/**
 * Created by milenkotomic on 14-05-15.
 */
function validateForms(button) {
    if (button == "save") {
        var saveButton = $("#saveButton");
        saveButton.attr('disabled', 'disabled');
    }
    var send = true;
    $("form#formID :input")
        .not(':hidden, :button, #id_exhibitor, #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time, #id_image').
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
    /*
    var fuData = $("#id_image");
    var FileUploadPath = fuData.val();

    if (fuData.length) {

        if (FileUploadPath != '') {
            var Extension = FileUploadPath.substring(
                FileUploadPath.lastIndexOf('.') + 1).toLowerCase();

            if (Extension != "gif" && Extension != "png" && Extension != "bmp"
                && Extension != "jpeg" && Extension != "jpg") {
                send = false;
                fuData.prev().prev().children('div').html("* Ingrese una imagen válida.");
            }
        }
        else {
            fuData.prev().prev().children('div').html("* Este campo es obligatorio.");
        }
    }
    */

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

    if (button == "save") {
        if (send)
            $("#processing").show();
        else
            saveButton.removeAttr('disabled');
    }
    return send;
}