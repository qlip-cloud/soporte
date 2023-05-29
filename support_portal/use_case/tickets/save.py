import frappe 

@frappe.whitelist()
def handler(subject, producto ,priority, tipo):


    doc = frappe.new_doc('Issue')
    doc.subject = subject
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.insert()

    frappe.db.commit()


    print(doc)
    
    return{
        #doc.insert()
       # "status":200, 
       # "data":{
       #     "status":status, 
       #     "subject":subject, 
       #     "priority":priority, 
       #     "tipo":tipo
       # }
    }



