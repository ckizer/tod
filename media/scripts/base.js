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

    function button_mouse_over(event){
	event.target.src = event.target.src.replace("_up.png","_over.png");
    }

    function button_mouse_out(event){
	event.target.src = event.target.src.replace("_over.png","_up.png");
	event.target.src = event.target.src.replace("_down.png","_up.png");
    }

    function button_mouse_down(event){
	event.target.src = event.target.src.replace("_over.png","_down.png");
    }

    function button_mouse_up(event){
	event.target.src = event.target.src.replace("_down.png","_over.png");
    }

function assign_behaviors() {
    $("#comment_area a").unbind("click").bind("click", toggle_comment_form);
    $("#cancel_comment").unbind("click").bind("click", toggle_comment_form);
    $("#submit_comment").unbind("click").bind("click", confirm_comment);
    $(".stated_button").unbind("mouseover").bind("mouseover", button_mouse_over);
    $(".stated_button").unbind("mouseout").bind("mouseout", button_mouse_out);
    $(".stated_button").unbind("mousedown").bind("mousedown", button_mouse_down);
    $(".stated_button").unbind("mouseup").bind("mouseup", button_mouse_up);
    $(".stated_button").unbind("drag").bind("drag", button_mouse_out);

}

$(document).ready(assign_behaviors);