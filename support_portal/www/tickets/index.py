import frappe
from support_portal.services.get_customer_id import handler as get_customer_id
from babel.dates import format_datetime

def get_context(context):
    
    #frappe.clear_cache()
        
    #frappe.website.render.clear_cache()
    
    context.no_cache = 1
    context.issues = frappe.db.get_list("Issue", filters = {"customer": get_customer_id(), "raised_by":frappe.session.user}, order_by='creation desc', fields = ["*"])
    context.status = frappe.db.get_list("Issue", filters = {"customer": get_customer_id(), "raised_by":frappe.session.user}, group_by='status', fields = ["status"])

    context.priorities = frappe.db.get_list("Issue Priority", fields = ["*"])

    for key, issue in enumerate(context.issues):
        context.issues[key].creation = format_datetime(issue.creation,format='short', locale='es_CO')
        context.issues[key].modified = format_datetime(issue.modified,format='short', locale='es_CO')

    










