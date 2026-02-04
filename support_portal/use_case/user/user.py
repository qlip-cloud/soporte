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
        return {"status": "success", "message": "Configuraciones guardadas correctamente."}
    except Exception as e:
        frappe.db.rollback()
        return {"status": "error", "message": str(e)}
    
@frappe.whitelist()
def create_contact_and_invite(user_data, customer_name):
    """
    Crea un contacto vinculado a un cliente y envía una invitación al usuario.
    El usuario recibe roles específicos y un correo de bienvenida.
    """
    try:
        user_data = json.loads(user_data)
        
        # Verificar si el usuario ya existe
        if frappe.db.exists("User", user_data.get("email")):
            return {"status": "error", "message": f"Usuario con el correo {user_data.get('email')} ya existe en el sistema."}

        # Creación de contacto vinculado al cliente
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": user_data.get("first_name"),
            "middle_name": user_data.get("middle_name"),
            "last_name": user_data.get("last_name"),
            "email_id": user_data.get("email"),
            "designation": user_data.get("designation"),
            "sp_pending_user_registration": 1
            # "user": new_user.name
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
        
        frappe.db.commit()

        user_created = False

        try:
            user = frappe.get_doc({
                "doctype": "User",
                "email": user_data.get("email"),
                "first_name": user_data.get("first_name"),
                "middle_name": user_data.get("middle_name"),
                "last_name": user_data.get("last_name"),
                "enabled": 1,
                "send_welcome_email": 0 
            })

            user.append("roles", {"role": "Customer"})
            user.append("roles", {"role": "Cliente Mentum"})

            user.insert(ignore_permissions=True)
            user_created = True

        except Exception as e:
            frappe.log_error(
                message=str(e),
                title="B2C invite flow"
            )

        if user_created:
            contact.user = user.name
            contact.sp_pending_user_registration = 0
            contact.save(ignore_permissions=True)
            message = (
                "Contacto y usuario creados correctamente. "
                "El usuario puede acceder al sistema."
            )
        else:
            message = (
                "Contacto creado correctamente. "
                "Se ha enviado una invitación al correo para completar el registro."
            )

        return {
            "status": "success",
            "message": message,
            "contact": contact.name,
            "user_created": user_created
        }
        
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error al crear el contacto y usuario: {str(e)}")
        frappe.throw(str(e))
        return {"status": "error", "message": str(e)}
