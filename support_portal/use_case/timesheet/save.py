import frappe 

def after_insert(timesheet, method):
    
    searched = []

    for time_detail in timesheet.time_logs:

        if time_detail.task not in searched:

            hours = frappe.db.get_list('Timesheet Detail',
                filters={'task': time_detail.task},
                fields=['*']
            )

            tah = 0
            tih = 0

            print(hours)

            for h in hours:
                tah += h.hours
                if h.is_billable:
                    tih += h.hours
            
            task = frappe.get_doc('Task', time_detail.task)
            task.horas_facturadas = tih
            task.horas_aplicadas = tah
            task.save()
            
        searched.append(time_detail.task)

    if method == "on_update":
        frappe.msgprint(f"Se han actualizados las horas")

    return timesheet




