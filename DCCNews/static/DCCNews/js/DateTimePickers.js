/**
 * Created by milenkotomic on 10-05-15.
 */

$(document).ready(function(){
    $("#id_start_circulation").datetimepicker({
        //sideBySide: true,
        format: 'DD-MM-YYYY',
        locale: 'es',
        showTodayButton: true
    }).on("dp.change", checkCirculation);

    $("#id_end_circulation").datetimepicker({
        //sideBySide: true,
        format: 'DD-MM-YYYY',
        locale: 'es',
        showTodayButton: true
    }).on("dp.change", checkCirculation);

});



function checkCirculation(){
    if ($.trim($('#id_start_circulation').val()) != '' && $.trim($('#id_end_circulation').val()) != ''){
        if (moment($("#id_start_circulation").val(), 'DD-MM-YYYY').isAfter(moment($("#id_end_circulation").val(), 'DD-MM-YYYY'))) {
            $("form#formID #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time")
                .each(function () {
                    $(this).parent().addClass("has-error")
                });
        }
        else if (moment($("#id_start_circulation").val(), 'DD-MM-YYYY').isSame(moment($("#id_end_circulation").val(), 'DD-MM-YYYY'))){
            if (moment($("#id_start_circulation_time").val(), 'hh:mm').toDate() >=
                moment($("#id_end_circulation_time").val(), 'hh:mm').toDate()){
                $("form#formID #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time")
                    .each(function () {
                        $(this).parent().addClass("has-error")
                    });
            }
            else{
                $("form#formID #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time")
                    .each(function () {
                        $(this).parent().removeClass("has-error")
                    });
            }
        }
        else{
            $("form#formID #id_start_circulation, #id_start_circulation_time, #id_end_circulation, #id_end_circulation_time")
                .each(function () {
                    $(this).parent().removeClass("has-error")
                });
        }
    }
}




