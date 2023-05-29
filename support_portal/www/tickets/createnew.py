import frappe

def get_context(context):
    
    context.issues = frappe.db.get_list("Issue", fields = ["*"])
    

@frappe.whitelist()
def handler(subject, producto ,priority, tipo):


    doc = frappe.new_doc('Issue')
    doc.subject = subject
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.insert()

    frappe.db.commit()
















