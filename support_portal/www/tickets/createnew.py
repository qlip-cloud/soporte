import frappe

def get_context(context):
    frappe.clear_cache()
        
    frappe.website.render.clear_cache()
    #context.issues = frappe.db.get_list("Issue", fields = ["*"])
    context.no_cache = 1
    context.products = frappe.db.get_list("Support product", fields = ["*"])
    context.types = frappe.db.get_list("Support type", fields = ["*"])
    context.priorities = frappe.db.get_list("Issue Priority", fields = ["*"])
    
    

@frappe.whitelist()
def handler(subject, producto ,priority, tipo):

    doc = frappe.new_doc('Issue')
    doc.subject = subject
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.via_customer_portal = True
    doc.insert()

    frappe.db.commit()

    var = {"id_control": doc.name}

    return var
















