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
            id:$(this).data("id"),
            priority:$("#priority").val(), 
            tipo:$("#tipo").val(),
            producto:$("#producto").val()      
        }
        method = "support_portal.use_case.tickets.update.handler"
        callback = (data) => {
            window.location.href = "/tickets";
        }
        send_petition(payload, method, callback)
    })

    $("#close").on("click", function(){
        payload={
            id:$(this).data("id")      
     
        }
        method = "support_portal.use_case.tickets.closeticket.handler"
        callback = (data) => {
            window.location.href = "/tickets";
        }
        send_petition(payload, method, callback)
    })

    $("#btn_comment").on("click", function(){
        payload={
            reference_doctype: "Issue",
            reference_name:$(this).data("id"), 
            content:$("#comment").val(),
            comment_email:$(this).data("user"),
            comment_by:   $(this).data("user") 
        }

        method = "frappe.desk.form.utils.add_comment"

        callback = (data) => {
            
            $("#comment").val("")

            date = new Date(data.creation);
            content = `
                <div style="margin-top: 20px">
                    ${data.comment_email} ${new Intl.DateTimeFormat('es-CO', { dateStyle: 'short', timeStyle: 'short' }).format(date)}:
                    <p>${data.content}</p>
                </div>
            `

            $("#comment_area").prepend(content)
            $('#blockscreen-modal').modal("hide")

        }

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

async function send_petition(payload, method, callresponse = null){
    $('#blockscreen-modal').modal("show")

    return new Promise(() => {
        frappe.call({
        method: method,
        args: payload,
        async: false,
        callback: function (result) {
            response = result.message

            callresponse(response)
                if (response.status && response.status == 400) {
                        
                    frappe.msgprint(__(`error: ${response.msg}`))
                }
            }    
        })
    })
}