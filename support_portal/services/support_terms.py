import frappe
from six import iteritems, string_types
from frappe.utils import today

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def handler(doctype, txt, searchfield, start, page_len, filters):

    condition = ""

    if filters:
        for fieldname, value in iteritems(filters):
            condition += " AND {field}={value}".format(
                    field=fieldname,
                    value=frappe.db.escape(value))
        
    return frappe.db.sql("""
        SELECT *
        FROM `tabSupport Terms`
        WHERE (
            (docstatus = 1
            AND cantidad_resta > 1   
            AND fecha_de_finalizacion > '{today}')
             AND restringir = 'No' 
        )   
        {condition}                            
        LIMIT %(start)s, %(page_len)s
        """.format(**{
        'condition': condition,
        'today':today()
        }), {
        'start': start,
        'page_len': page_len
    })