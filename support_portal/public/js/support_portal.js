
function search_items_options_by_customer() {

    $('#blockscreen-modal').modal("show")

    url = "/api/method/support_portal.services.get_customer_band_product.handler"

    callback = (array) => {

        var allowedValues = array.map(function (item) {
            return item.support_product;
        });

        $('#producto option').each(function () {
            if (!allowedValues.includes($(this).val())) {
                $(this).hide();
            }
        });

        $('#blockscreen-modal').modal("hide")

    }
    send_petition_upload("", "", null, callback, url)
}

function send_petition_upload(module_root, method, formData, callback, url = null) {

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
        xhr.open('POST', endpoint, true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);
        xhr.send(formData);

    })
}