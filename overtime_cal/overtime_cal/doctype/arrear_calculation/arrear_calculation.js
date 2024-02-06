// Copyright (c) 2024, erpdata and contributors
// For license information, please see license.txt



// get table arrear sheet details and Total arrear for employee
frappe.ui.form.on('Arrear Calculation', {
	calculate_arrear: function(frm) {
		frm.clear_table("arrear_sheet");
		frm.refresh_field('arrear_sheet');
		frm.clear_table("total_arrear_for_employee");
		frm.refresh_field('total_arrear_for_employee');
		frm.call({
			method:'get_arrear_sheet',
			doc:frm.doc
		})
	}
});

// based on filter get employee from employee doctype
frappe.ui.form.on('Arrear Calculation', {
	get_employee_details: function(frm) {
		frm.clear_table("employee_list");
		frm.refresh_field('employee_list');
		frm.call({
			method:'get_employee',
			doc:frm.doc
		})
	}
});

// after check all check all employee in employee list
frappe.ui.form.on('Arrear Calculation', {
	check_all: function(frm) {
		frm.call({
			method:'checkall',
			doc:frm.doc
		})
	}
});

