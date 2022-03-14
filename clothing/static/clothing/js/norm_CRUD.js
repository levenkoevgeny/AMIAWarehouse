$('#add_norm_item_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'norm': $('#id_norm').val(),
        'clothes': $('#id_clothes').val() == "" ? null : $('#id_clothes').val(),
        'norm_count': $('#id_norm_count').val() == "" ? null : $('#id_norm_count').val(),
        'wear_time': $('#id_wear_time').val() == "" ? null : $('#id_wear_time').val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();
    fetch('/api/norms-items/', {
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


$('.norm_item_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'norm': $(`#id_norm`).val(),
        'clothes': $(`#id_clothes_${form_id}`).val() == "" ? null : $(`#id_clothes_${form_id}`).val(),
        'norm_count': $(`#id_norm_count_${form_id}`).val() == "" ? null : $(`#id_norm_count_${form_id}`).val(),
        'wear_time': $(`#id_wear_time_${form_id}`).val() == "" ? null : $(`#id_wear_time_${form_id}`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/norms-items/${form_id}/`, {
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


function delete_item_in_norm(id) {
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/norms-items/${id}/`, {
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

$('.norm_update_form').submit(function (e) {
    e.preventDefault();
    let norm_id = $(`#id_norm_id`).val()
    let obj = {
        'norm_title': $(`#id_norm_title`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/norms/${norm_id}/`, {
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

$('#add_norm_form').submit(function (e) {
    e.preventDefault();
    let url = $('#id_parent_norm').val() == "" ? "/api/norms/" : "/clothing/norms/make-clone/"
    let new_obj = {
        'norm_title': $('#id_norm_title').val() == "" ? null : $('#id_norm_title').val(),
        'created_at': new Date(),
        'parent_norm': $('#id_parent_norm').val() == "" ? null : $('#id_parent_norm').val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(url, {
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