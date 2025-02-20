import frappe
from frappe.model.document import Document
import appraise.controllers.form_validation as validation
import appraise.controllers.aggregatorController as agg
import re

Doctype = 'Developing and imparting people skills'
pattern_for_wtg = r'\((\s*(?:\d+\.\d+|\d+)\s*)\)'


class Developingandimpartingpeopleskills(Document):
    """method to autoname your document"""
    def autoname(self):
        self.name = f'PDB1_{self.owner}_{self.academic_year}_{self.semester}'
    
    def before_save(self):
        self.self_appraisal_score = compute_marks(self)
        agg.modify(self, Doctype)

    def validate(self):
        validation.standard_validation(self)


    def on_trash(self):
        agg.delete(self)


def compute_marks(self):

    counter = 0
    pas = []

    for item in self.criteria_table:
        if counter > 1:
            frappe.throw('Can only have two entries in the table')
        else:
            counter += 1

            match = re.search(pattern_for_wtg, item.col1)
            if match:
                val1 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            match = re.search(pattern_for_wtg, item.col2)
            if match:
                val2 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            marks_obtained = val1 * val2 * 400
            item.col3 = marks_obtained

            pas.append(marks_obtained)
    
    final_sum = sum(pas)
    if final_sum > 480:
        return 480
    else:
        return round(final_sum)
