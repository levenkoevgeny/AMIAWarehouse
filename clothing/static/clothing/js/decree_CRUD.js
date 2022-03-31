$('#add_decree_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'employee': $('#id_employee_hidden').val(),
        'decree_start': $('#id_decree_start').val(),
        'decree_finish': $('#id_decree_finish').val() == "" ? null : $('#id_decree_finish').val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();

    fetch('/api/employees-decrees/', {
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


$('.decree_update_form').submit(function (e) {
    e.preventDefault();

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let decree_id = e.target.id;


    let obj = {
        'employee': $(`#id_employee_hidden`).val(),
        'decree_start': $(`#id_decree_start_${decree_id}`).val(),
        'decree_finish': $(`#id_decree_finish_${decree_id}`).val() === "" ? null : $(`#id_decree_finish_${decree_id}`).val(),
    }


    fetch(`/api/employees-decrees/${decree_id}/`, {
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


function delete_decree(id) {
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/employees-decrees/${id}/`, {
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