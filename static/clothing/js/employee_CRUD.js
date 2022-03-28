$('#add_employee_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
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

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch('/api/employees/', {
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

$('.employee_update_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'last_name': $(`#id_last_name_${form_id}`).val() == "" ? null : $(`#id_last_name_${form_id}`).val(),
        'first_name': $(`#id_first_name_${form_id}`).val() == "" ? null : $(`#id_first_name_${form_id}`).val(),
        'patronymic': $(`#id_patronymic_${form_id}`).val() == "" ? null : $(`#id_patronymic_${form_id}`).val(),
        'personal_number': $(`#id_personal_number_${form_id}`).val() == "" ? null : $(`#id_personal_number_${form_id}`).val(),
        'kind': $(`#id_kind_${form_id}`).val() == "" ? null : $(`#id_kind_${form_id}`).val(),
        'subdivision': $(`#id_subdivision_${form_id}`).val() == "" ? null : $(`#id_subdivision_${form_id}`).val(),
        'rank': $(`#id_rank_${form_id}`).val() == "" ? null : $(`#id_rank_${form_id}`).val(),
        'position': $(`#id_position_${form_id}`).val() == "" ? null : $(`#id_position_${form_id}`).val(),
        'group': $(`#id_group_${form_id}`).val() == "" ? null : $(`#id_group_${form_id}`).val(),
        'sex': $(`#id_sex_${form_id}`).val() == "" ? null : $(`#id_sex_${form_id}`).val(),
        'date_of_birth': $(`#id_date_of_birth_${form_id}`).val() == "" ? null : $(`#id_date_of_birth_${form_id}`).val(),
        'enlisted': $(`#id_enlisted_${form_id}`).val() == "" ? null : $(`#id_enlisted_${form_id}`).val(),
        'excluded': $(`#id_excluded_${form_id}`).val() == "" ? null : $(`#id_excluded_${form_id}`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/employees/${form_id}/`, {
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