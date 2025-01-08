$(document).ready(function () {

    search_items_options_by_customer()
    $("#save").on("click", function () {
        payload = {
            subject: $("#subject").val(),
            producto: $("#producto").val(),
            priority: $("#priority").val(),
            tipo: $("#tipo").val(),
            description: $("#description").val(),
            comment: $("#comment").val(),
            customer: $("#customer").val()
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
    $("#imgInp").on("change", function () {
        $("#upload_picture").modal("hide")
        filename = $('#imgInp').val()
        $("#adjuntado").text("✔ " + filename.substring(12))
        $("#adjuntado").show()

    })
})

function update(id_control) {
    fileToUpload = $('#imgInp').prop('files');

    if ($('#imgInp').val()) {

        var formData = new FormData();

        url = "/api/method/upload_file"

        formData.append("file", fileToUpload[0], fileToUpload[0].name);

        formData.append("is_private", 0);
        formData.append("doctype", "Issue");
        formData.append("docname", id_control);
        formData.append("fieldname", "image");

        callback = (data) => {

            window.location.href = "/tickets/"
        }

        send_petition_upload("", "", formData, callback, url)
    } else {
        window.location.href = "/tickets/"
    }
}


async function send_petition(payload, method, callresponse = null) {
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

