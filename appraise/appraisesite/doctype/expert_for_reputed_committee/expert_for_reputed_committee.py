import frappe
from frappe.model.document import Document
import appraise.controllers.form_validation as validation
import appraise.controllers.aggregatorController as agg
import re

Doctype = 'Expert for reputed committee'
pattern_for_wtg = r'\((\s*(?:\d+\.\d+|\d+)\s*)\)'


class Expertforreputedcommittee(Document):
    """method to autoname your document"""
    def autoname(self):
        self.name = f'CB2_{self.owner}_{self.academic_year}_{self.semester}'
    
    def before_save(self):
        self.self_appraisal_score = compute_marks(self)
        agg.modify(self, Doctype)

    def validate(self):
        validation.standard_validation(self)

        if self.num1 > 1:
            frappe.throw('Violation in first criterion: PA committee has set max number of appointments to not exceed 1')
        if self.num2 > 1:
            frappe.throw('Violation in second criterion: PA committee has set max number of appointments to not exceed 1')
        if self.num3 > 1:
            frappe.throw('Violation in third criterion: PA committee has set max number of appointments to not exceed 1')

    def on_trash(self):
        agg.delete(self)


def compute_marks(self):

    self.m1 = self.num1 * 50
    self.m2 = self.num2 * 40
    self.m3 = self.num3 * 30

    marks_obtained = self.m1 + self.m2 + self.m3
    
    return marks_obtained
