import frappe

def get_context(context):
    
    
    
    context.issues = frappe.db.get_list("Issue", fields = ["*"])
    










