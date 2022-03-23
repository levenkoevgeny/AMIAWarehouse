$('#add_norm_item_form').submit(function (e) {
    e.preventDefault();
    let new_item = {
        'item_clothes': $(`#id_item_clothes`).val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();
    fetch('/api/norms-items/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(new_item)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
        .finally(() => window.location.href = window.location.href)
});

function delete_norm_item(id) {
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


$('.norm_item_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let new_item = {
        'item_clothes': $(`#id_item_clothes_${form_id}`).val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    console.log(new_item);

    show_spinner();
    fetch(`/api/norms-items/${form_id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(new_item)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message))
        .finally(() => window.location.href = window.location.href)
});