function show_spinner() {
    $('#id_main_div').css('height', '100vh')
        .addClass('d-flex justify-content-center align-items-center')
        .html('<div class="d-flex justify-content-center">\n' +
        '  <div class="spinner-border text-secondary" style="width: 3rem; height: 3rem;" role="status">\n' +
        '    <span class="visually-hidden">Loading...</span>\n' +
        '  </div>\n' +
        '</div>');
}


$('#clothes_in_card_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    let ids_array = $('#id_clothes').val();

    let requests = [];
    ids_array.map(id => {
        let new_obj = {
            'card': $('#id_card').val(),
            'clothes': id,
            'count': $('#id_count_of_issue').val(),
            'date_of_issue': $('#id_date_of_issue').val(),
            'movement': $('#id_movement').val(),
            'has_certificate': $('#id_has_certificate_checkbox').is(':checked'),
            'certificate_number': $('#id_certificate_number').val() == "" ? null : $('#id_certificate_number').val(),
            'document_number': $('#id_document_number').val() == "" ? null : $('#id_document_number').val(),
        }

        requests.push(
            fetch('/api/clothes-in-card/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(new_obj)
            })
        )
    })

    show_spinner();

    Promise.all(requests).then(() => {
        window.location.href = window.location.href
    }).catch((e) => alert(e.message));
});

$('#add_card_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'card_number': $('#id_card_number').val() == "" ? null : $('#id_card_number').val(),
        'employee': $('#id_employee').val() == "" ? null : $('#id_employee').val(),
        'norm': $('#id_norm').val() == "" ? null : $('#id_norm').val(),
        'growth': $('#id_growth').val() == "" ? null : $('#id_growth').val(),
        'bust': $('#id_bust').val() == "" ? null : $('#id_bust').val(),
        'jacket': $('#id_jacket').val() == "" ? null : $('#id_jacket').val(),
        'shoes': $('#id_shoes').val() == "" ? null : $('#id_shoes').val(),
        'cap': $('#id_cap').val() == "" ? null : $('#id_cap').val(),
        'collar': $('#id_collar').val() == "" ? null : $('#id_collar').val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch('/api/cards/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(new_obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            window.location.href = window.location.href
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
});


$('#id_employee_update_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let id_employee = $("#id_employee").val();
    let obj = {
        'last_name': $(`#id_last_name`).val() == "" ? null : $(`#id_last_name`).val(),
        'first_name': $(`#id_first_name`).val() == "" ? null : $(`#id_first_name`).val(),
        'patronymic': $(`#id_patronymic`).val() == "" ? null : $(`#id_patronymic`).val(),
        'subdivision': $(`#id_subdivision`).val() == "" ? null : $(`#id_subdivision`).val(),
        'sex': $(`#id_sex`).val() == "" ? null : $(`#id_sex`).val(),
        'kind': $(`#id_kind`).val() == "" ? null : $(`#id_kind`).val(),
        'rank': $(`#id_rank`).val() == "" ? null : $(`#id_rank`).val(),
        'position': $(`#id_position`).val() == "" ? null : $(`#id_position`).val(),
        'date_of_birth': $(`#id_date_of_birth`).val() == "" ? null : $(`#id_date_of_birth`).val(),
    }

    show_spinner();

    fetch(`/api/employees/${id_employee}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            window.location.href = window.location.href
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
});


$('#id_card_data_update_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let id_card = $("#id_card").val();
    let obj = {
        'norm': $(`#id_norm`).val(),
        'growth': $(`#id_growth`).val() == "" ? null : $(`#id_growth`).val(),
        'bust': $(`#id_bust`).val() == "" ? null : $(`#id_bust`).val(),
        'jacket': $(`#id_jacket`).val() == "" ? null : $(`#id_jacket`).val(),
        'shoes': $(`#id_shoes`).val() == "" ? null : $(`#id_shoes`).val(),
        'cap': $(`#id_cap`).val() == "" ? null : $(`#id_cap`).val(),
        'collar': $(`#id_collar`).val() == "" ? null : $(`#id_collar`).val(),
    }

    show_spinner();

    fetch(`/api/cards/${id_card}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            window.location.href = window.location.href
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
});


$('.clothes_in_card_update_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let form_id = e.target.id;

    let obj = {
        'movement': $(`#id_movement_modal_${form_id}`).val(),
        'count': $(`#id_count_modal_${form_id}`).val(),
        'date_of_issue': $(`#id_date_of_issue_modal_${form_id}`).val(),
        'has_replacement': $(`#id_has_replacement_modal_${form_id}`).is(':checked'),
        'has_certificate': $(`#id_has_certificate_checkbox_modal_${form_id}`).is(':checked'),
        'certificate_number': $(`#id_certificate_number_${form_id}`).val() == "" ? null : $(`#id_certificate_number_${form_id}`).val(),
        'document_number': $(`#id_document_number_${form_id}`).val() == "" ? null : $(`#id_document_number_${form_id}`).val(),
    }

    show_spinner();

    fetch(`/api/clothes-in-card/${form_id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            window.location.href = window.location.href
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
});