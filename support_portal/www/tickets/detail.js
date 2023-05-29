$(document).ready(function() {

    $("#upload").on("click", function(){

        id_control = $(this).data('id')
        
        fileToUpload = $('#imgInp').prop('files');
    
        if ($('#imgInp').val()){
    
    //      $(".picture-loading").html("Cargando...")
       
            var formData = new FormData();
    
            url = "/api/method/upload_file"
    
            formData.append("file", fileToUpload[0], fileToUpload[0].name);
    
    
            formData.append("is_private", 0);
            formData.append("doctype", "Issue");
            formData.append("docname", id_control);
            formData.append("fieldname", "image");
    
            callback = (data)=>{
    
                $(".modal").modal("hide")
            //    $(".picture-loading").html("")            
            //    $("#blah").prop("src", "https://via.placeholder.com/150")
            //    $(`#${img_control}`).prop("src", data.file_url)          
            //    $('#imgInp').val("")
            //    $("#image").val(data.file_url)

            console.log(data)
    
            //    payload = {
            //      company_id:id_control,
            //      image: data.file_url
            //    }
    
            //    send_petition(payload, UPDATE_IMAGE_ROOT,"update")
    
            }
    
            send_petition_upload("", "", formData, callback, url)
        }else{
            $(".picture-loading").html("Debe seleccionar una imagen")
        }
    })

    $("#save").on("click", function(){
        payload={
            subject:$("#subject").val(),
            producto:$("#producto").val(), 
            priority:$("#priority").val(), 
            tipo:$("#tipo").val()       
        }
        method = "support_portal.use_case.tickets.save.handler"
        callback = (data) => {window.location.href = "/tickets";}
        send_petition(payload, method, callback)
    })


})


function send_petition_upload(module_root, method, formData, callback, url = null, raise_exception = true){

    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = () => {
            if (xhr.readyState == XMLHttpRequest.DONE) {

                response = JSON.parse(xhr.responseText)

                if (xhr.status === 200) {

                   
                    callback(response.message)

                } else {
                   
                    callback(response.message)
                   
                    if (raise_exception){
                   
                        frappe.msgprint(__(`Error: ${response.message.msg}`));
                    }

                }
            }
        }

        endpoint = url ? url : setup_method(API_ROOT, module_root, method, true)

        console.log(endpoint)
       
        xhr.open('POST',endpoint , true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);
        xhr.send(formData);

    })
}

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