function toggle_comment_form(event) {
    /*    console.log("clicked toggle_comment_form"); */
    $("#comment_form").slideToggle();
    event.preventDefault();
}

    function confirm_comment(event){
	/*	console.log("clicked submit button"); */
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
    
    function set_focus() {
	var start_heres = $(".start_here");
	var element_to_focus = false;
	if(start_heres) {
	    var first_start_here = start_heres[0];
	    if(first_start_here) {
		if(first_start_here.is("input")) {
		    // The first marked element is the start here
		    element_to_focus = first_start_here;
		} else {
		    // Find the first input in the start here block element
		    var contained_element = first_start_here.find("input");
		    if(contained_element) {
			element_to_focus = contained_element
		    }
		}
	    }
	}
	var forms = $("form");
	if(forms) {
	    var inputs = forms.find("input");
	    if( inputs ) {
		var first_input = inputs[0];
		if( $(first_input).is("input")) {
		    element_to_focus = first_input;
		}
	    }
	}
	if(element_to_focus) {
	    element_to_focus.focus();
	}
    }

    $(document).ready(assign_behaviors);
    $(document).ready(set_focus);
