function activate_tabs() {
    // Make tabs clickable
    $("#tab-container a[role='tab']").click(function(e) {
	e.preventDefault();
	var target = $(e.target);
	if ($(e.target).prop('tagName')!='A') {
	    target = $(e.target).parents('a');
	}
	var tab_id = target.attr('href');
	if (tab_id != window.location.hash) {
	    window.location.hash = tab_id;
	    $(this).tab('show');
	}
    });

    // Click a default tab
    var start_tab_hash = "#plain";
    var first_hash = window.location.hash;
    if ($("#tab-container a[href='"+first_hash+"']").length > 0) {
	start_tab_hash = first_hash;
    }
    window.location.hash = "";
    $("#tab-container a[href='"+start_tab_hash+"']").click();
}

function email_main(){
    setTimeout(activate_tabs, 1); // Timeout necessary to prevent auto-scroll to hash
}

$(email_main);
