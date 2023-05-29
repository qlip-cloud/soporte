import frappe

def get_context(context):

    query_params = frappe.request.args
    code = query_params.get("code")

    context.issue = frappe.get_doc("Issue", code)





@frappe.whitelist()
def handler(subject, producto ,priority, tipo):

    doc = frappe.get_doc('Issue', subject)
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.save()
    frappe.db.commit()









    










