import frappe 
from frappe import _

def after_insert(issue, method):
    
    print("issue " + method)

    task = frappe.get_doc({
        'doctype': 'Task',
        'subject': issue.subject,
        'issue':issue.name
    })

    task.insert()

    frappe.msgprint(f"Se ha creado la tarea {task.name}")

    return task

def update(issue, method):

    print("issue " + method)

    if issue.support_terms:
        sup_ter = frappe.db.get_list('Issue',
                    filters={'support_terms': issue.support_terms},
                    fields=['*']
                )

        tah = 0
        tih = 0

        for t in sup_ter:
            if sup_ter.status == _("Closed"):
                tah += t.horas_aplicadas
                tih += t.horas_facturadas

        support_term = frappe.get_doc('Support Terms', issue.support_terms)
        

        if support_term.tipo_de_asignacion == "Número de casos":
            support_term.cantidad_aplicada = len(sup_ter)
            support_term.cantidad_facturada = len(sup_ter)
        if support_term.tipo_de_asignacion == "Número de Horas":
            support_term.cantidad_aplicada = tah
            support_term.cantidad_facturada = tih

        if support_term.cantidad_total:
            support_term.cantidad_descontable = support_term.cantidad_total - support_term.cantidad_facturada
        else:
            support_term.cantidad_descontable = support_term.cantidad_facturada
            
        support_term.save()

    return issue



