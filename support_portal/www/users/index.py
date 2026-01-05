import frappe
from support_portal.services.get_customer_id import handler as get_customer_id
from support_portal.services.users import get_users_by_customer


def get_context(context):

  context.no_cache = 1
  frappe.clear_cache()      
  frappe.website.render.clear_cache()
  context.page_name = "Usuarios"
  
  # User authentication
  context.customer = get_customer_id()
  context.users = get_users_by_customer(context.customer[0].name)
  user = frappe.session.user
  if user == "Guest":
    frappe.local.flags.redirect_location = "/login"
    raise frappe.Redirect
  

  
  return context