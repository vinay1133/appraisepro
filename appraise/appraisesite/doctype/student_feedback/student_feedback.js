let templateString = frappe.boot.my_global_template
let modifiedString = templateString.replace("{{DocType}}", "Student Feedback");
eval(modifiedString);