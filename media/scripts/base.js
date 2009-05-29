function toggle_comment_form(event) {
//    console.log("clicked toggle_comment_form");
    $("#comment_form").slideToggle();
    event.preventDefault();
}

function assign_behaviors() {
    $("#comment_area a").unbind("click").bind("click", toggle_comment_form);
    $("#cancel_comment").unbind("click").bind("click", toggle_comment_form);
}

$(document).ready(assign_behaviors);