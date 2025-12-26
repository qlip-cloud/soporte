import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def upload_file_portal(doctype, docname, is_private=0):
    user = frappe.session.user

    if user == "Guest":
        frappe.throw("No autorizado")

    if not frappe.has_permission(doctype, "write", docname):
        frappe.throw("Sin permiso")

    uploaded = frappe.request.files.get("file")
    if not uploaded:
        frappe.throw("Archivo no recibido")

    return save_file(
      uploaded.filename,
      uploaded.stream.read(),
      doctype,
      docname,
      is_private=is_private
  )

