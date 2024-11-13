frappe.ui.form.on("Issue", "customer", function(frm, cdt, cdn){
    frm.set_query("support_terms", function() {
        return {
            "filters": {
                "cliente": frm.doc.customer
            }
        };
    })
});