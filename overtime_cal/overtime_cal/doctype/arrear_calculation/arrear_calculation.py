# Copyright (c) 2024, erpdata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class ArrearCalculation(Document):

	# get employee based on filter of department and branch
	@frappe.whitelist()   
	def get_employee(self):
		doc = frappe.get_all("Employee", 
						filters={"status":self.status,"department":self.department,"branch":self.branch},
						fields=["employee","employee_name"],)
		if(doc):
			for d in doc:
				self.append('employee_list', {
											"employee_id":d.employee,
											"employee_name":d.employee_name,})
				
 	
	# after check all button select all employee
	@frappe.whitelist()
	def checkall(self):
		children = self.get('employee_list')
		if not children:
			return
		all_selected = all([child.check for child in children])  
		value = 0 if all_selected else 1 
		for child in children:
			child.check = value
   		
		
	# calculate arrear amount
	@frappe.whitelist()
	def calculate_arrear(self, emp):
		total = 0
		doc = frappe.get_value("Salary Structure Assignment", {"employee": emp.employee, "employee_name": emp.employee_name}, "salary_structure")
		base = frappe.get_value("Salary Structure Assignment", {"employee": emp.employee, "employee_name": emp.employee_name}, "base")
		if doc:
			new_list = [{'base':base if base else 0 , 'formula': None}]
			doc1 = frappe.get_doc('Salary Structure', doc)
			for i in doc1.get('earnings'):
				amount = float(i.get('amount', 0))
				abbr = i.get('abbr')
				formula =i.get('formula') if i.get('formula') else None
				earning_dict = {abbr: amount, 'formula': formula}
				new_list.append(earning_dict)    
				for variable in new_list:
					if variable['formula']:
						variables = {k: new_list[i][k] for i in range(new_list.index(variable)) for k in new_list[i] if k != 'formula'} 
						result = eval(variable['formula'], {**variables, **globals()})
						new_list[new_list.index(variable)][list(variable.keys())[0]] = result
				filtered_list = [item for item in new_list if 'base' not in item]
				total = 0
				for item in filtered_list:
					amount = list(item.values())[0]
					total_amount = amount * float(emp.payment_days) / int(emp.total_working_days)
					total += total_amount

			return total
		else:
			frappe.msgprint("No 'earnings' data found in the document.")
			return 0

	# get amount the revised salary based on new assigned salary structure
	@frappe.whitelist()
	def get_arrear_sheet(self):
		for i in self.get('employee_list'):
			if i.check:
				if self.from_date and self.to_date:
					emp_salary_slip = frappe.get_all("Salary Slip",
													filters={"posting_date": ["between", [self.from_date, self.to_date]],
															"employee": i.employee_id, "status": "Submitted"},
													fields=["employee", "employee_name", "posting_date", "gross_pay", "payment_days", "salary_structure", "total_working_days", "payment_days"])
					
					if emp_salary_slip:
						for emp in emp_salary_slip:
							self.append('arrear_sheet', {
								"employee_id": emp.employee,
								"employee_name": emp.employee_name,
								"date": emp.posting_date,
								"basic_salary": emp.gross_pay,
								"revised_salary": self.calculate_arrear(emp),
								"amount_differance": self.calculate_arrear(emp) - emp.gross_pay,
							})							
		self.get_total_arrear()


	# Calculate total Arrear Amount for each employee
	@frappe.whitelist()
	def get_total_arrear(self):
		employee_id_dict = {}
		for i in self.get('arrear_sheet'):
			if i.employee_id not in employee_id_dict:
				employee_id_dict[i.employee_id] = {
					"employee_id": i.employee_id,
					"employee_name": i.employee_name,
					"arrear_amount": i.amount_differance,
					"date":self.arrear_creadited_date,
	
				}
			else:
				employee_id_dict[i.employee_id]['arrear_amount'] += i.amount_differance

		for data in employee_id_dict:
			self.append('total_arrear_for_employee', {
				"employee_id": employee_id_dict[data]['employee_id'],
				"employee_name": employee_id_dict[data]['employee_name'],
				"arrear_amount": employee_id_dict[data]['arrear_amount'],
				"date":self.arrear_creadited_date,

	
			})


