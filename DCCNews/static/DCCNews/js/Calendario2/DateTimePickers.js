/**
 * Created by milenkotomic on 10-05-15.
 */

$(document).ready(function(){
    $("#id_start_circulation").datetimepicker({
        sideBySide: true,
        format: 'DD-MM-YYYY HH:mm'
    }).on("dp.change", checkCirculation);

    $("#id_end_circulation").datetimepicker({
        sideBySide: true,
        format: 'DD-MM-YYYY HH:mm'
    }).on("dp.change", checkCirculation);

});



function checkCirculation(){
    if ($.trim($('#id_start_circulation').val()) != '' && $.trim($('#id_end_circulation').val()) != ''){
        if (moment($("#id_start_circulation").val(), 'DD-MM-YYYY HH:mm').toDate() >
            moment($("#id_end_circulation").val(), 'DD-MM-YYYY HH:mm').toDate()){
            $("#id_start_circulation").parent().addClass("has-error");
            $("#id_end_circulation").parent().addClass("has-error");
        }
        else{
            $("#id_start_circulation").parent().removeClass("has-error");
            $("#id_end_circulation").parent().removeClass("has-error");
        }
    }
}

//$("#id_end_circulation").datetimepicker()


