import frappe
def handler():

    email = frappe.session.user

    sql = """SELECT 
                customer.name as name
            FROM
                tabContact as contact
            inner join
                `tabDynamic Link` as link
                on (contact.name = link.parent)
            inner join
                `tabCustomer` as customer
                on(link.link_name = customer.name)
            where contact.email_id = '{}';""".format(email)
    
    result =  frappe.db.sql(sql, as_dict=1)

    if result:

        return result[0]["name"]
    
    frappe.throw("Usuario no configurado")