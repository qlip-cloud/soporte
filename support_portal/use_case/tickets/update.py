import frappe 

@frappe.whitelist()
def handler(id,priority, tipo, producto):


    doc = frappe.get_doc('Issue', id)
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.save()

    frappe.db.commit()


    print(doc)
    
    return{
       "status":200
       # "data":{
       #     "status":status, 
       #     "subject":subject, 
       #     "priority":priority, 
       #     "tipo":tipo
       # }
    }



