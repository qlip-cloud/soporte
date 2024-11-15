import frappe

def update(support_terms, method):

    print("support_terms " + method)

    sup_ter = frappe.db.get_list('Issue',
                filters={'support_terms': support_terms.name},
                fields=['*']
            )

    tah = 0
    tih = 0

    for t in sup_ter:
        tah += t.horas_aplicadas    
        tih += t.horas_facturadas   

    if support_terms.tipo_de_asignacion == "Número de casos":
        support_terms.cantidad_aplicada = len(sup_ter)
        support_terms.cantidad_facturadas = len(sup_ter)
    if support_terms.tipo_de_asignacion == "Número de Horas":
        support_terms.cantidad_aplicada = tah
        support_terms.cantidad_facturadas = tih

    if support_terms.cantidad_total:
        support_terms.cantidad_descontable = support_terms.cantidad_total - support_terms.cantidad_facturadas
    else:
        support_terms.cantidad_descontable = support_terms.cantidad_facturadas

    return support_terms