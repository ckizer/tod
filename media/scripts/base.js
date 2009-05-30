function toggle_comment_form(event) {
//    console.log("clicked toggle_comment_form");
    $("#comment_form").slideToggle();
    event.preventDefault();
}

    function confirm_comment(event){
//	console.log("clicked submit button");
	alert("Thank you for your input");
	toggle_comment_form;
    }

function assign_behaviors() {
    $("#comment_area a").unbind("click").bind("click", toggle_comment_form);
    $("#cancel_comment").unbind("click").bind("click", toggle_comment_form);
    $("#submit_comment").unbind("click").bind("click", confirm_comment);
}

$(document).ready(assign_behaviors);