import frappe

@frappe.whitelist()
def set_arrear(payroll_entry):
    start_date, end_date = frappe.get_value("Payroll Entry", {"name": payroll_entry}, ["start_date", "end_date"])
    child_data = frappe.get_all("Payroll Employee Detail", {"parent": payroll_entry}, "employee")

    for i in child_data:
        total_arrear_amount = frappe.get_value("Total Arrear Calculated", {"date": ["between", [start_date, end_date]], "employee_id": i.employee}, "arrear_amount")

        salary_slip = frappe.get_value("Salary Slip", {"payroll_entry": payroll_entry, "employee": i.employee}, "name")

        if total_arrear_amount:
            doc = frappe.get_doc("Salary Slip", salary_slip)
            arrear_exists = any(e.salary_component == "Arrear" for e in doc.earnings)

            if not arrear_exists:
                doc.append("earnings", {
                    "salary_component": "Arrear",
                    "amount": total_arrear_amount,
                })
                doc.save()
