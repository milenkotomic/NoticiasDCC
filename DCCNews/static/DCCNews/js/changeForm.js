/**
 * Created by milenkotomic on 26-05-15.
 */

function goToPrev(template) {
    document.form.action = "/news/visualize/" + template + "/";
}

function goToSave(){
    document.form.action = "";
}
