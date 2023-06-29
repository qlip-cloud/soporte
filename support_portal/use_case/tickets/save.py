import frappe 
from  frappe.desk.form.utils import add_comment


@frappe.whitelist()
def handler(subject, producto ,priority, tipo, description, comment):

    doc = frappe.new_doc('Issue')
    doc.subject = subject
    doc.priority = priority
    doc.tipo = tipo
    doc.producto = producto
    doc.description = description
    doc.insert()

   
    user = frappe.session.user


    resp = add_comment(reference_doctype= "Issue", reference_name= doc.name, content=comment, comment_email= user, comment_by= user)
    print(resp)

    frappe.db.commit()

    frappe.clear_cache()

    frappe.website.render.clear_cache()
    
    var = {
       "status":200,
       "id_control": doc.name
    }

    print(var)
    return var



