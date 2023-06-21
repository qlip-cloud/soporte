import frappe

def get_context(context):
    
    #context.issues = frappe.db.get_list("Issue", fields = ["*"])

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
    doc.insert()

    frappe.db.commit()

    var = {"id_control": doc.name}
    print(var)

    return var
















