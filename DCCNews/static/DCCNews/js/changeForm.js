/**
 * Created by milenkotomic on 26-05-15.
 */

function goToPrev(template) {
    document.form.action = "/news/visualize/" + template + "/";
    document.form.target = "_blank";
    document.form.setAttribute("onsubmit", "return validateForms('prev')");
}

function goToSave(){
    document.form.action = "";
    document.form.target = "_self";
    document.form.setAttribute("onsubmit", "return validateForms('save')");
}
