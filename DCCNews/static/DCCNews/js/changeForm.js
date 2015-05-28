/**
 * Created by milenkotomic on 26-05-15.
 */

function goToPrev(template) {
    document.form.action = "/news/visualize/" + template + "/";
    document.form.target = "_blank"
}

function goToSave(){
    document.form.action = "";
    document.form.target = "_self"
}
