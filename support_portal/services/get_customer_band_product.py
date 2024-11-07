import frappe
@frappe.whitelist()
def handler():

    email = frappe.session.user

    sql = """SELECT 
                band_support_product.support_product as support_product,
                band_support_product.band as band
                
            FROM
                tabContact as contact
            inner join
                `tabDynamic Link` as link
                on (contact.name = link.parent)
            inner join
                `tabCustomer` as customer
                on(link.link_name = customer.name)
                
            inner join
                `tabBand_Support_Product` as band_support_product
                on(band_support_product.parent = customer.name)
                
            where contact.email_id = '{}';""".format(email)
    
    result =  frappe.db.sql(sql, as_dict=1)

    if result:

        return result
    
    frappe.throw("Usuario no configurado")