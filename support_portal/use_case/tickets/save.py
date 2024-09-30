import frappe 
from  frappe.desk.form.utils import add_comment


@frappe.whitelist()
def handler(subject, producto ,priority, tipo, description, comment):

    doc = frappe.new_doc('Issue')

    contact_doc_name = frappe.db.get_value('Contact', filters={'user': frappe.session.user_email}, fieldname=['name'])

    if contact_doc_name:
      client_doc_name = frappe.db.get_value('Dynamic Link', filters={'parenttype': 'Contact', 'link_doctype':'Customer', 'parent':contact_doc_name}, fieldname=['link_name'],)

      if client_doc_name:
            band_support_product_list = frappe.db.get_list('Dynamic Link', filters={'parenttype': 'Cliente', 'link_doctype':'Band_Support_Product', 'parent':client_doc_name}, fields=['*'],)

            exist = False

            if band_support_product_list:
                for b in band_support_product_list:
                    if b.support_product == producto:
                        exist = True
                        doc.band = b.band
                        break
                    
            if not exist:
               client_band = frappe.db.get_value('Cliente', filters={'name':client_doc_name}, fieldname=['band'],)
               doc.band = client_band
    
    
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



