import frappe
from babel.dates import format_datetime
from support_portal.services.get_customer_id import handler as get_customer_id

def get_context(context):
    frappe.clear_cache()
        
    frappe.website.render.clear_cache()
    query_params = frappe.request.args

    code = query_params.get("code")

    context.issue = get_issue(code)
    
    context.products = frappe.db.get_list("Support product", fields = ["*"])
    context.types = frappe.db.get_list("Support type", fields = ["*"])
    context.priorities = frappe.db.get_list("Issue Priority", fields = ["*"])
    context.user = frappe.session.user

    context.comments = frappe.db.get_list("Comment", filters = { "reference_doctype": "Issue", "reference_name": code}, fields = ["*"])
    
    for key, comment in enumerate(context.comments):
        
        context.comments[key].creation = format_datetime(comment.creation,format='short', locale='es_CO')
    


@frappe.whitelist()
def handler(subject, producto ,priority, tipo):

    doc = frappe.get_doc('Issue', subject)
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.save()
    frappe.db.commit()

def get_issue(code):

    result = frappe.db.get_list("Issue", filters = {"name": code, "customer": get_customer_id()}, fields = ["*"])
    
    if result:

        return result[0]
    
    raise Exception("Usuario no permitido")






    










