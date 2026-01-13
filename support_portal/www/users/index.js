$(document).ready(function () {
  const initialStates = {};
  $('input[type="checkbox"][name="enabled"]').each(function (index) {
    initialStates[index] = $(this).is(':checked');
  });

  $('input[type="checkbox"][name="enabled"]').on('change', function () {
    let hasChanges = false;

    $('input[type="checkbox"][name="enabled"]').each(function (index) {
      if ($(this).is(':checked') !== initialStates[index]) {
        hasChanges = true;
        return false;
      }
    });
    if (hasChanges) {
      $('#save-button-container').slideDown();
    } else {
      $('#save-button-container').slideUp();
    }
  });
  $('#save-settings').on('click', function () {
    const settings = [];
    $('input[type="checkbox"][name="enabled"]').each(function () {
      settings.push({
        id: $(this).data('id'),
        enabled: $(this).is(':checked') ? 1 : 0
      });
    });
    const payload = { settings: settings };
    const method = "support_portal.use_case.user.user.save_users_settings";
    const callback = (response) => {
      if (response.status === 'success') {
        frappe.msgprint({
          title: 'Success',
          message: __('Cambios guardados exitosamente.'),
          indicator: 'green'
        });
        $('#save-button-container').slideUp();
        Object.keys(initialStates).forEach(index => {
          initialStates[index] = $('input[type="checkbox"][name="enabled"]').eq(index).is(':checked');
        });
      } else {
        frappe.msgprint({
          title: 'Error',
          message: __('Error al guardar los cambios. Por favor, inténtelo de nuevo.'),
          indicator: 'red'
        });
      }
    };
    console.log("Payload:", payload);
    frappe.call({
      method: method,
      args: payload,
      callback: function (data) {
        callback(data.message);
      }
    });
  });
  $('#create-new-user').on('click', function () {
    const newUser = {
      email: $('#new-user-email').val(),
      first_name: $('#new-user-first-name').val(),
      middle_name: $('#new-user-middle-name').val(),
      last_name: $('#new-user-last-name').val(),
      designation: $('#new-user-designation').val(),
      username: $('#new-user-username').val()
    };

    if (!newUser.email || !newUser.first_name || !newUser.last_name || !newUser.designation) {
      frappe.msgprint({
        title: 'Error',
        message: __('Por favor, complete todos los campos obligatorios.'),
        indicator: 'red'
      });
      return;
    }

    customer = $('#customer').val();
    const customerArray = JSON.parse(customer.replace(/'/g, '"'));
    const customer_name = customerArray[0].name;

    const method = "support_portal.use_case.user.user.create_contact_and_invite";
    const callback = (response) => {
      if (response.status === 'success') {
        frappe.msgprint({
          title: 'Success',
          message: __('Usuario creado exitosamente.'),
          indicator: 'green',
        });
        window.location.reload();
      } else {
        frappe.msgprint({
          title: 'Error',
          message: __('Error al crear el usuario: {0}', [response.message || 'Por favor, inténtelo de nuevo.']),
          indicator: 'red'  
        });
        
      }
    };
    $('#blockscreen-modal').modal("show")
    frappe.call({
      method: method,
      args: { user_data: newUser, customer_name: customer_name },
      callback: function (data) {
        callback(data.message);

      }
    });
  });
});