import frappe 

@frappe.whitelist()
def handler(id):


    doc = frappe.get_doc('Issue', id)
    doc.status = "Closed"
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



