function delete_clothes(id) {
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/clothes/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
    }).then(response => {
            if (response.status >= 200 && response.status < 300) {
                window.location.href = window.location.href
            } else {
                throw new Error("Ошибка удаления!")
            }
        }
    ).catch((e) => alert(e.message))
}

$('#clothes_add_form').submit(function (e) {
    e.preventDefault();
    new_obj = {
        'clothes_title': $(`#id_clothes_title`).val(),
        'nomenclature': $(`#id_nomenclature`).val() == "" ? null : $('#id_nomenclature').val(),
        'wear_time': $(`#id_wear_time`).val()
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch('/api/clothes/', {
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

$('.clothes_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    obj = {
        'clothes_title': $(`#id_clothes_title_${form_id}`).val(),
        'nomenclature': $(`#id_nomenclature_${form_id}`).val() == "" ? null : $(`#id_nomenclature_${form_id}`).val(),
        'wear_time': $(`#id_wear_time_${form_id}`).val()
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/clothes/${form_id}/`, {
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