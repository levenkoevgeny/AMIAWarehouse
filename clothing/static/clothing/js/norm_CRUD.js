$('#add_norm_item_form').submit(function (e) {
    e.preventDefault();
    new_obj = {
        'norm': $('#id_norm').val(),
        'clothes': $('#id_clothes').val() == "" ? null : $('#id_clothes').val(),
        'norm_count': $('#id_norm_count').val() == "" ? null : $('#id_norm_count').val(),
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch('/api/norms-items/', {
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


$('.norm_item_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    obj = {
        'norm': $(`#id_norm`).val(),
        'clothes': $(`#id_clothes_${form_id}`).val() == "" ? null : $(`#id_clothes_${form_id}`).val(),
        'norm_count': $(`#id_norm_count_${form_id}`).val() == "" ? null : $(`#id_norm_count_${form_id}`).val(),
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/norms-items/${form_id}/`, {
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


function delete_item_in_norm(id) {
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/norms-items/${id}/`, {
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

$('.norm_update_form').submit(function (e) {
    e.preventDefault();
    let norm_id = $(`#id_norm_id`).val()
    obj = {
        'norm_title': $(`#id_norm_title`).val(),
    }
    console.log(obj);
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/norms/${norm_id}/`, {
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

$('#add_norm_form').submit(function (e) {
    e.preventDefault();
    let url = $('#id_parent_norm').val() == "" ? "/api/norms/" : "/clothing/norms/make-clone/"
    new_obj = {
        'norm_title': $('#id_norm_title').val() == "" ? null : $('#id_norm_title').val(),
        'created_at': new Date(),
        'parent_norm': $('#id_parent_norm').val() == "" ? null : $('#id_parent_norm').val(),
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(url, {
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