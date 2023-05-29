
$(document).ready(function() {
    $("#save").on("click", function(){
        payload={
            subject:$("#subject").val(),
            producto:$("#producto").val(), 
            priority:$("#priority").val(), 
            tipo:$("#tipo").val()       
        }
        method = "customer_support.use_case.tickets.save.handler"
        callback = (data) => {window.location.href = "/tickets";}
        send_petition(payload, method, callback)
    })
})

async function send_petition(payload, method, callresponse = null){
     return new Promise(() => {
         frappe.call({
         method: method,
         args: payload,
         async: false,
         callback: function (result) {
                     response = result.message
                             if (response.status == 200) {
                                            if (callresponse) {
                                                callresponse(response)
                                            }
                                        }
                                        if (response.status == 400) {
                                            if (callresponse) {
                                                callresponse(response.data)
                                            }
                                            frappe.msgprint(__(`error: ${response.msg}`))
                                        }
                                    }    
         })
     })
}

