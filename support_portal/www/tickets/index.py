import frappe

def get_context(context):
    
    frappe.clear_cache()
        
    frappe.website.render.clear_cache()
    
    context.issues = frappe.db.get_list("Issue", fields = ["*"])

    










