let templateString = frappe.boot.my_global_template
let modifiedString = templateString.replace("{{DocType}}", "Course Result");
eval(modifiedString);
