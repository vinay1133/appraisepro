import frappe
from frappe.model.document import Document
import appraise.controllers.form_validation as validation
import appraise.controllers.aggregatorController as agg
import re

Doctype = 'Papers published in national or international journal'
pattern_for_wtg = r'\((\s*(?:\d+\.\d+|\d+)\s*)\)'


class Paperspublishedinnationalorinternationaljournal(Document):
    """method to autoname your document"""
    def autoname(self):
        self.name = f'RB2_{self.owner}_{self.academic_year}_{self.semester}'
    
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

            match = re.search(pattern_for_wtg, item.col3)
            if match:
                val3 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            match = re.search(pattern_for_wtg, item.col4)
            if match:
                val4 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            match = re.search(pattern_for_wtg, item.col5)
            if match:
                val5 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            match = re.search(pattern_for_wtg, item.col6)
            if match:
                val6 = float(match.group(1).strip())
            else:
                frappe.throw('Error Fetching Field Weightages')

            # marks obtained column
            marks_obtained = round(val1 * val2 * val3 * val4 * val5 * val6 * 100, 2)
            item.col7 = marks_obtained

            pas.append(marks_obtained)

    return round(sum(pas))
