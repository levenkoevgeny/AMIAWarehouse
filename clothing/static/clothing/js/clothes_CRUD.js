$('#clothes_add_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'clothes_title': $(`#id_clothes_title`).val(),
        'nomenclature': $(`#id_nomenclature`).val() == "" ? null : $('#id_nomenclature').val(),
        'wear_time': $(`#id_wear_time`).val(),
        'price': $(`#id_price`).val() == "" ? null : $('#id_price').val(),
        'has_to_be_deposited': $(`#id_has_to_be_deposited`).is(':checked'),
        'created_at': new Date(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch('/api/clothes/', {
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
    }).catch((e) => alert(e.message))
        .finally(() => window.location.href = window.location.href)
});

function delete_clothes(id) {
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/clothes/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
    }).then(response => {
            if (response.status >= 200 && response.status < 300) {
            } else {
                throw new Error("Ошибка удаления!")
            }
        }
    ).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
}

$('.clothes_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'clothes_title': $(`#id_clothes_title_${form_id}`).val(),
        'nomenclature': $(`#id_nomenclature_${form_id}`).val() == "" ? null : $(`#id_nomenclature_${form_id}`).val(),
        'wear_time': $(`#id_wear_time_${form_id}`).val(),
        'price': $(`#id_price_${form_id}`).val() == "" ? null : $(`#id_price_${form_id}`).val(),
        'has_to_be_deposited': $(`#id_has_to_be_deposited`).is(':checked'),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/clothes/${form_id}/`, {
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
    }).catch((e) => alert(e.message))
        .finally(() => window.location.href = window.location.href)
});