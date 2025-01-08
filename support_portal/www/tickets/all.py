import json
import frappe
from support_portal.services.get_customer_id import handler as get_customer_id
from babel.dates import format_datetime

def get_context(context):

    #frappe.clear_cache()
        
    #frappe.website.render.clear_cache()
    
    context.no_cache = 1

    query_params = frappe.request.args

    context.customers = get_customer_id()

    if query_params.get("customer"):
        context.customer = query_params.get("customer")
    else:
        context.customer = context.customers[0]['name']

    context.issues = frappe.db.get_list("Issue", filters = {"customer": context.customer}, order_by='creation desc', fields = ["*"])

    for key, issue in enumerate(context.issues):
        print(json.loads(issue._assign)[0])
        context.issues[key].assign = json.loads(issue._assign)[0] if issue._assign else ''
        context.issues[key].creation = format_datetime(issue.creation,format='short', locale='es_CO')
        context.issues[key].modified = format_datetime(issue.modified,format='short', locale='es_CO')

    










