frappe.ui.form.on("Issue", {
    customer: function(frm, cdt, cdn){
        frm.set_query("support_terms", function() {
            return {
                query:"support_portal.services.support_terms.handler",
                filters: {"cliente": frm.doc.customer}
            };
        });
        frm.refresh_fields()
    }
});