$('#add_employee_form').submit(function (e) {
    e.preventDefault();
    new_obj = {
        'last_name': $('#id_last_name').val() == "" ? null : $('#id_last_name').val(),
        'first_name': $('#id_first_name').val() == "" ? null : $('#id_first_name').val(),
        'patronymic': $('#id_patronymic').val() == "" ? null : $('#id_patronymic').val(),
        'subdivision': $('#id_subdivision').val() == "" ? null : $('#id_subdivision').val(),
        'sex': $('#id_sex').val() == "" ? null : $('#id_sex').val(),
        'kind': $('#id_kind').val() == "" ? null : $('#id_kind').val(),
        'rank': $('#id_rank').val() == "" ? null : $('#id_rank').val(),
        'position': $('#id_position').val() == "" ? null : $('#id_position').val(),
        'date_of_birth': $('#id_date_of_birth').val() == "" ? null : $('#id_date_of_birth').val(),
    }

    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch('/api/employees/', {
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

$('.employee_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    obj = {
        'last_name': $(`#id_last_name_${form_id}`).val() == "" ? null : $(`#id_last_name_${form_id}`).val(),
        'first_name': $(`#id_first_name_${form_id}`).val() == "" ? null : $(`#id_first_name_${form_id}`).val(),
        'patronymic': $(`#id_patronymic_${form_id}`).val() == "" ? null : $(`#id_patronymic_${form_id}`).val(),
        'subdivision': $(`#id_subdivision_${form_id}`).val() == "" ? null : $(`#id_subdivision_${form_id}`).val(),
        'sex': $(`#id_sex_${form_id}`).val() == "" ? null : $(`#id_sex_${form_id}`).val(),
        'kind': $(`#id_kind_${form_id}`).val() == "" ? null : $(`#id_kind_${form_id}`).val(),
        'rank': $(`#id_rank_${form_id}`).val() == "" ? null : $(`#id_rank_${form_id}`).val(),
        'position': $(`#id_position_${form_id}`).val() == "" ? null : $(`#id_position_${form_id}`).val(),
        'date_of_birth': $(`#id_date_of_birth_${form_id}`).val() == "" ? null : $(`#id_date_of_birth_${form_id}`).val(),
    }
    csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    fetch(`/api/employees/${form_id}/`, {
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