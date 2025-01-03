import frappe
from babel.dates import format_datetime
from support_portal.services.get_customer_id import handler as get_customer_id

def get_context(context):
    #frappe.clear_cache()
        
    #frappe.website.render.clear_cache()
    query_params = frappe.request.args

    code = query_params.get("code")

    context.no_cache = 1
    context.issue = get_issue(code)
    
    context.products = frappe.db.get_list("Support product", fields = ["*"])
    context.types = frappe.db.get_list("Support type", fields = ["*"])
    context.priorities = frappe.db.get_list("Issue Priority", fields = ["*"])
    context.user = frappe.session.user


    comments = frappe.db.get_list("Comment", filters = { "reference_doctype": "Issue", "reference_name": code}, fields = ["*"])
    communications = frappe.db.get_list("Communication", filters = { "reference_doctype": "Issue", "reference_name": code}, fields = ["*"])

    for key, comment in enumerate(comments):
        comments[key].creation = format_datetime(comment.creation,format='short', locale='es_CO')

    for key, communications in enumerate(communications):
        communications[key].creation = format_datetime(communications.creation,format='short', locale='es_CO')
    
    context.comments = sorted(comments + communications, key=lambda i: i['creation'], reverse=True)


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






    










