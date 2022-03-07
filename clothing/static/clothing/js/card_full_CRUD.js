$('#clothes_in_card_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    let ids_array = $('#id_clothes').val();

    let requests = []
    ids_array.map(id => {
        let new_obj = {
            'card': $('#id_card').val(),
            'clothes': id,
            'count': $('#id_count_of_issue').val(),
            'date_of_issue': $('#id_date_of_issue').val()
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

    Promise.all(requests).then(() => {
        window.location.href = window.location.href
    }).catch((e) => alert(e.message))
});

function delete_clothes_in_card(id) {
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/clothes-in-card/${id}/`, {
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

$('.clothes_in_card_update_form').submit(function (e) {
    e.preventDefault();
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let form_id = e.target.id;

    let obj = {
        'count': $(`#id_count_${form_id}`).val(),
        'date_of_issue': $(`#id_date_of_issue_${form_id}`).val(),
        'has_replacement': $(`#id_has_replacement_${form_id}`).is(':checked')
    }

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