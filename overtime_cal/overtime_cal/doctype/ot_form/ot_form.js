// Copyright (c) 2023, erpdata and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Form', {
	// refresh: function(frm) {
	
	// }
});



frappe.ui.form.on('OT Form', {
	setup: function (frm) {
        // Fetch the current user's name and set it to the Supervisor Name field
		frappe.call({
            method: 'get_current_user_name',
			doc:frm.doc
			
        });
    }
});


