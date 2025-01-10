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
        context.customer = context.customers[0]['tax_id']

    customer = frappe.db.get_value('Customer', {'tax_id': context.customer}, ['name'])
    context.issues = frappe.db.get_list("Issue", filters = {"customer": customer, "raised_by":frappe.session.user}, order_by='creation desc', fields = ["*"])

    for key, issue in enumerate(context.issues):

        assignments = frappe.db.get_list("ToDo", filters = dict(reference_type = 'Issue', reference_name = issue.name, status = ('!=', 'Cancelled')), fields = ['owner', 'name'])
        
        assignments_list = []

        for assign in assignments:
           assignments_list.append(frappe.db.get_value('User', {'email': assign.owner}, ['full_name']))

        context.issues[key].assign = ', '.join(assignments_list) if assignments_list else ''
        context.issues[key].creation = format_datetime(issue.creation,format='short', locale='es_CO')
        context.issues[key].modified = format_datetime(issue.modified,format='short', locale='es_CO')

    










