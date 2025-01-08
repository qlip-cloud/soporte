import frappe
from support_portal.services.get_customer_id import handler as get_customer_id
from babel.dates import format_datetime

def get_context(context):

    #frappe.clear_cache()
        
    #frappe.website.render.clear_cache()
    
    context.no_cache = 1

    query_params = frappe.request.args

    context.customers = get_customer_id()
    context.customer = None

    if query_params:
        context.customer = query_params.get("customer")
    else:
        context.customer = context.customers[0]['name']

    context.issues = frappe.db.get_list("Issue", filters = {"customer": context.customer}, order_by='creation desc', fields = ["*"])

    for key, issue in enumerate(context.issues):
        context.issues[key].assign = issue._assing[0]
        context.issues[key].creation = format_datetime(issue.creation,format='short', locale='es_CO')
        context.issues[key].modified = format_datetime(issue.modified,format='short', locale='es_CO')

    










