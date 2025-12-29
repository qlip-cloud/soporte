import frappe
from frappe.utils import nowdate

def restrict_support_terms():
    frappe.db.sql("""
        UPDATE `tabSupport Terms`
        SET restringir = 'Si'
        WHERE
            docstatus = 1
            AND restringir = 'No'
            AND fecha_de_finalizacion <= %(today)s
    """, {
        "today": nowdate()
    })

    frappe.db.commit()
