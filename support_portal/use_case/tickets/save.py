import frappe 
from  frappe.desk.form.utils import add_comment


@frappe.whitelist()
def handler(subject, producto ,priority, tipo, description, comment, customer):

   doc = frappe.new_doc('Issue')
   doc.subject = subject
   doc.priority = priority
   doc.tipo = tipo
   doc.producto = producto
   doc.description = description
   doc.via_customer_portal = True
   doc.customer = customer

   # band section
   contact_doc_name = frappe.db.get_value('Contact', filters={'email_id': frappe.session.user}, fieldname=['name'])

   if contact_doc_name:
      client_doc_name = frappe.db.get_value('Dynamic Link', filters={'parenttype': 'Contact', 'link_doctype':'Customer', 'parent':contact_doc_name}, fieldname=['link_name'])

      if client_doc_name:        
            
            band_support_product_list = frappe.db.get_list('Band_Support_Product', filters={'parent': client_doc_name, 'parenttype':'Customer'}, fields=['*'])

            exist = False

            if band_support_product_list:
                  for b in band_support_product_list:
                     if b.support_product == doc.producto:
                        exist = True
                        doc.band = b.band
                        break
                  
            if not exist:
               client_band = frappe.db.get_value('Customer', filters={'name':client_doc_name}, fieldname=['band'])
               doc.band = client_band

   # end band section

   doc.insert()

   user = frappe.session.user

   resp = add_comment(reference_doctype= "Issue", reference_name= doc.name, content=comment, comment_email= user, comment_by= user)

   frappe.db.commit()

   frappe.clear_cache()

   frappe.website.render.clear_cache()
    
   var = {
      "status":200,
      "id_control": doc.name
   }

   return var



