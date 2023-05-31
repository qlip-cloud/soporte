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
    
    return{
       "status":200
       # "data":{
       #     "status":status, 
       #     "subject":subject, 
       #     "priority":priority, 
       #     "tipo":tipo
       # }
    }



