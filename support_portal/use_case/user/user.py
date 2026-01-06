import frappe
import json

@frappe.whitelist()
def save_users_settings(settings):
    """Save user-specific settings."""
    try:
        # Parse the JSON string to a list
        if isinstance(settings, str):
            settings = json.loads(settings)
        
        for sett in settings:
            user_id = sett.get("id")
            enabled = sett.get("enabled")
            user_doc = frappe.get_doc("User", user_id)
            user_doc.enabled = enabled
            user_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": "User settings saved successfully."}
    except Exception as e:
        frappe.db.rollback()
        return {"status": "error", "message": str(e)}
    
@frappe.whitelist()
def create_user(user_data, customer_name):
    """
    Crear usuario en el sistema con los datos proporcionados.
    Crear un contacto vinculado al usuario creado y al cliente correspondiente.
    Enviar correo de bienvenida al nuevo usuario.
    """
    try:
        user_data = json.loads(user_data)
        
        # Verificar si el usuario ya existe
        if frappe.db.exists("User", user_data.get("email")):
            return {"status": "error", "message": f"User with email {user_data.get('email')} already exists"}
            frappe.throw(f"User with email {user_data.get('email')} already exists")
        
        # Creación de usuario
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": user_data.get("email"),
            "first_name": user_data.get("first_name"),
            "middle_name": user_data.get("middle_name"),
            "last_name": user_data.get("last_name"),
            "username": user_data.get("username"),
            "enabled": 1,
            "send_welcome_email": 1  
        })
        
        # Añadir roles antes del insert
        new_user.append("roles", {"role": "Customer"})
        new_user.append("roles", {"role": "Cliente Mentum"})
        
        new_user.insert(ignore_permissions=True)
        
        # Creación de contacto vinculado al cliente
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "designation": user_data.get("designation"),
            "user": new_user.name
        })
        
        # Añadir email al contacto
        contact.append("email_ids", {
            "email_id": user_data.get("email"),
            "is_primary": 1
        })
        
        # Vincular contacto al cliente
        contact.append("links", {
            "link_doctype": "Customer",
            "link_name": customer_name
        })
        
        contact.insert(ignore_permissions=True)
        
        # Commit después de crear ambos documentos
        frappe.db.commit()
        
        
        return {
            "status": "success", 
            "message": "User and contact created successfully.",
            "user": new_user.name,
            "contact": contact.name
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in create_user: {str(e)}")
        frappe.throw(str(e))
        return {"status": "error", "message": str(e)}
