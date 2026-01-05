import frappe


def get_customer_contacts(customer):
    """Get all contacts associated with a specific customer.""" 
    query = """
        SELECT
            contact.name AS contact_name,
            contact.email_id AS email,
            contact.user AS user
        FROM
            `tabContact` AS contact
        Inner JOIN
            `tabDynamic Link` AS link
        ON
            contact.name = link.parent
        Inner JOIN
            `tabCustomer` AS customer
        ON
            link.link_name = customer.name
        WHERE
            customer.name = %s AND contact.user IS NOT NULL
    """
    contacts = frappe.db.sql(query, (customer,), as_dict=True)
    return contacts

def get_users_by_customer(customer):
    """Get all users associated with a specific customer."""
    contacts = get_customer_contacts(customer)
    users = []
    for contact in contacts:
        user_doc = frappe.get_doc("User", contact.user)
        users.append({
            "name": user_doc.name,
            "email": contact.email,
            "enabled": user_doc.enabled
        })
    return users