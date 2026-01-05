import frappe
from frappe.utils import nowdate

def restrict_support_terms():
    to_restrict_terms = frappe.get_all("Support Terms", filters={
        "docstatus": 1,
        "restringir": "No",
        "fecha_de_finalizacion": ("<=", nowdate())
    }, fields=["name"])
    for term in to_restrict_terms:
        support_term = frappe.get_doc("Support Terms", term.name)
        support_term.restringir = "Si"
        support_term.save(ignore_permissions=True)



