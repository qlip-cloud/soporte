$(document).ready(function() {
    $("#save").on("click", function(){
        payload={
            subject:$("#subject").val(),
            producto:$("#producto").val(), 
            priority:$("#priority").val(), 
            tipo:$("#tipo").val(),
            description:$("#description").val(), 
            comment:$("#comment").val()
            }
        method = "support_portal.use_case.tickets.save.handler"
        callback = (data) => {
            console.log("data", data)
        //    window.location.href = "/tickets";
            update(data.id_control)
        }
        console.log(payload, method)
        send_petition(payload, method, callback)
    })
})

function send_petition_upload(module_root, method, formData, callback, url = null){

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = () => {
            if (xhr.readyState == XMLHttpRequest.DONE) {
            $('#blockscreen-modal').modal("hide")

                response = JSON.parse(xhr.responseText)
                
                callback(response.message)

            }
        }

        endpoint = url ? url : setup_method(API_ROOT, module_root, method, true)      
        xhr.open('POST',endpoint , true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);
        xhr.send(formData);

    })
}


function update(id_control){
    fileToUpload = $('#imgInp').prop('files');
    console.log(fileToUpload)
    console.log($('#imgInp').val())
    if ($('#imgInp').val()){
           
        var formData = new FormData();

        url = "/api/method/upload_file"

        formData.append("file", fileToUpload[0], fileToUpload[0].name);

        formData.append("is_private", 0);
        formData.append("doctype", "Issue");
        formData.append("docname", id_control);
        formData.append("fieldname", "image");

        callback = (data)=>{

            window.location.href = "/tickets"
        }

        send_petition_upload("", "", formData, callback, url)
    }else{
        window.location.href = "/tickets"
    }
}


async function send_petition(payload, method, callresponse = null){
    $('#blockscreen-modal').modal("show")

     return new Promise(() => {
         frappe.call({
         method: method,
         args: payload,
         async: false,
         callback: function (result) {
                     response = result.message
                     console.log(result.message)
                     console.log(result)
                     if (callresponse) {
                        callresponse(response)
                    }
                            // if (response.status == 200) {
                            //                if (callresponse) {
                            //                    callresponse(response)
                            //                }
                            //            }
                            //            if (response.status == 400) {
                            //                if (callresponse) {
                            //                    callresponse(response.data)
                            //                }
                            //                frappe.msgprint(__(`error: ${response.msg}`))
                            //            }
                                    }    
         })
     })
}

