import frappe 

def update(task, method):
    
    print("task " + method)
    
    tasks = frappe.db.get_list('Task',
                filters={'issue': task.issue},
                fields=['*']
            )

    tah = 0
    tih = 0

    for t in tasks:
        tah += t.horas_aplicadas
        tih += t.horas_facturadas

    issue = frappe.get_doc('Issue', task.issue)
    issue.horas_facturadas = tih
    issue.horas_aplicadas = tah
    issue.save()

    return task




