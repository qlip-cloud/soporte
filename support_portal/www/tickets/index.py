import frappe
from support_portal.services.get_customer_id import handler as get_customer_id

def get_context(context):
    
    frappe.clear_cache()
        
    frappe.website.render.clear_cache()
    
    context.issues = frappe.db.get_list("Issue", filters = {"customer": get_customer_id()}, fields = ["*"])

    










