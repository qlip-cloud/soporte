import frappe

def link_user_to_pending_contact(doc, method):
    """
    Después de crear un usuario, buscar si hay un contacto pendiente
    con el mismo email y vincularlo.
    """
    try:
        contacts = frappe.get_all(
            "Contact Email",
            filters={
                "email_id": doc.email
            },
            fields=["parent"]
        )
        
        if not contacts:
            return
        
        for contact_email in contacts:
            contact = frappe.get_doc("Contact", contact_email.parent)
            
            # Solo vincular si el contacto está pendiente y no tiene usuario asignado
            if (hasattr(contact, 'custom_pending_user_registration') and 
                contact.custom_pending_user_registration == 1 and 
                not contact.user):
                
                contact.user = doc.name
                contact.custom_pending_user_registration = 0
                contact.save(ignore_permissions=True)
                
                frappe.logger().info(
                    f"Linked user {doc.name} to contact {contact.name}"
                )
                
                
    except Exception as e:
        frappe.log_error(
            message=f"Error linking user {doc.email} to contact: {str(e)}",
            title="User-Contact Linking Error"
        )