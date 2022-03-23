$('#clothes_in_card_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let norm_items_array = $('#id_norm_items').val();

    let description_requests = [];

    let count = $('#id_count_of_issue').val();

    norm_items_array.map(id => {

        let new_movement = {
            "norm_item": id,
            'created_at': new Date(),
            'date_of_issue': $('#id_date_of_issue').val(),
            "movement_direction": $('#id_movement').val(),
            "has_replacement": false,
            "document_number": $('#id_document_number').val() == "" ? null : $('#id_document_number').val(),
            "has_certificate": $('#id_has_certificate_checkbox').is(':checked'),
            "certificate_number": $('#id_certificate_number').val() == "" ? null : $('#id_certificate_number').val(),
            "is_closed_loop": $('#id_is_closed_loop').is(':checked'),
            "card": $('#id_card').val(),
        }

        show_spinner();

        fetch('/api/movements/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(new_movement)
        }).then(response => response.json()
            .then(movement => {
                    fetch(`/api/norms-items/${id}/`).then(response => response.json())
                        .then(norm_item => {
                            norm_item.item_clothes.map(item_id => {
                                let new_description = {
                                    "count": count,
                                    "movement": movement.id,
                                    "clothes": item_id
                                }

                                description_requests.push(
                                    fetch('/api/description-item/', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json;charset=utf-8',
                                            "X-CSRFToken": csrftoken,
                                        },
                                        body: JSON.stringify(new_description)
                                    })
                                )
                            })
                            Promise.all(description_requests).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href);
                        })
                }
            ))
    })

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

    show_spinner();

    fetch('/api/cards/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(new_obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
});


$('#id_employee_update_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let id_employee = $("#id_employee").val();
    let obj = {
        'last_name': $('#id_last_name').val() == "" ? null : $('#id_last_name').val(),
        'first_name': $('#id_first_name').val() == "" ? null : $('#id_first_name').val(),
        'patronymic': $('#id_patronymic').val() == "" ? null : $('#id_patronymic').val(),
        'personal_number': $('#id_personal_number').val() == "" ? null : $('#id_personal_number').val(),
        'kind': $('#id_kind').val() == "" ? null : $('#id_kind').val(),
        'subdivision': $('#id_subdivision').val() == "" ? null : $('#id_subdivision').val(),
        'rank': $('#id_rank').val() == "" ? null : $('#id_rank').val(),
        'position': $('#id_position').val() == "" ? null : $('#id_position').val(),
        'group': $('#id_group').val() == "" ? null : $('#id_group').val(),
        'sex': $('#id_sex').val() == "" ? null : $('#id_sex').val(),
        'date_of_birth': $('#id_date_of_birth').val() == "" ? null : $('#id_date_of_birth').val(),
        'enlisted': $('#id_enlisted').val() == "" ? null : $('#id_enlisted').val(),
        'excluded': $('#id_excluded').val() == "" ? null : $('#id_excluded').val(),
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
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
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
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
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
        'certificate_number': $(`#id_certificate_number_modal_${form_id}`).val() == "" ? null : $(`#id_certificate_number_modal_${form_id}`).val(),
        'document_number': $(`#id_document_number_modal_${form_id}`).val() == "" ? null : $(`#id_document_number_modal_${form_id}`).val(),
    }

    if (obj.has_certificate) {
        obj.document_number = null
    } else {
        obj.certificate_number = null
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
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
});