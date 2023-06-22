import frappe 

@frappe.whitelist()
def handler(subject, producto ,priority, tipo, description):


    doc = frappe.new_doc('Issue')
    doc.subject = subject
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.description = description
    doc.insert()

    frappe.db.commit()

    print(doc)

    frappe.clear_cache()

    frappe.website.render.clear_cache()
    
    var = {
       "status":200,
       "id_control": doc.name
    }

    print(var)
    return var



