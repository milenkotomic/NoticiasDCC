/**
 * Created by milenkotomic on 10-05-15.
 */

$(document).ready(function(){
    $("#id_start_circulation").datetimepicker({
        sideBySide: true,
        format: 'dd-mm-yyyy hh:ii',
        linkField: "hide_start_cirulation",
        linkFormat: 'yyyy-mm-ddThh:ii',
        autoclose: true,
        weekStart: 1,
        todayBtn: true,
        todayHighlight: true,

    });
    $("#id_end_circulation").datetimepicker({
        sideBySide: true,
        format: 'dd-mm-yyyy hh:ii',
        linkField: "hide_end_cirulation",
        linkFormat: 'yyyy-mm-ddThh:ii',
        autoclose: true,
        weekStart: 1,
        todayBtn: true,
        todayHighlight: true

    });
});

function checkCirculation(){
    if (new Date($("#hide_start_cirulation").val()) && new Date($("#hide_end_cirulation").val())){
        if (new Date($("#hide_start_cirulation").val()) >= new Date($("#hide_end_cirulation").val())){
            $("#id_start_circulation").parent().addClass("has-error");
            $("#id_end_circulation").parent().addClass("has-error");
        }
        else{
            $("#id_start_circulation").parent().removeClass("has-error");
            $("#id_end_circulation").parent().removeClass("has-error");
        }
    }
}
