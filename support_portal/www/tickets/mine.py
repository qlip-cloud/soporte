import frappe
from support_portal.services.get_customer_id import handler as get_customer_id

def get_context(context):
    
    print(context)

    #frappe.clear_cache()
        
    #frappe.website.render.clear_cache()
    
    context.no_cache = 1
    context.issues = frappe.db.get_list("Issue", filters = {"customer": get_customer_id(), "raised_by":frappe.session.user}, fields = ["*"])

    










