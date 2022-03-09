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

$('#add_card_form').submit(function (e) {
    e.preventDefault();
    new_obj = {
        'employee': $('#id_employee').val() == "" ? null : $('#id_employee').val(),
        'norm': $('#id_norm').val() == "" ? null : $('#id_norm').val(),
        'growth': $('#id_growth').val() == "" ? null : $('#id_growth').val(),
        'bust': $('#id_bust').val() == "" ? null : $('#id_bust').val(),
        'jacket': $('#id_jacket').val() == "" ? null : $('#id_jacket').val(),
        'shoes': $('#id_shoes').val() == "" ? null : $('#id_shoes').val(),
        'cap': $('#id_cap').val() == "" ? null : $('#id_cap').val(),
        'collar': $('#id_collar').val() == "" ? null : $('#id_collar').val(),
    }

    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
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