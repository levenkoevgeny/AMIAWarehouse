$("#id_all_position_checkbox").change(function () {
    let norm_id = $('#id_norm').val();

    let norm;
    let norm_array = []

    if (this.checked) {
        fetch(`/api/norms-items/?norm=${norm_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
        }).then(response => response.json())
            .then(norm_json => {
                norm = norm_json;
                norm.forEach(element => norm_array.push(element.clothes.toString()))
                $('#id_clothes').val(norm_array);
                $('#id_clothes').trigger('change');
            })
    } else {
        $('#id_clothes').val([]);
        $('#id_clothes').trigger('change');
    }
});


$("#id_has_certificate_checkbox").change(function () {
    if (this.checked) {
        $('#id_certificate_number').prop("disabled", false);
        $('#id_document_number').prop("disabled", true);

    } else {
        $('#id_certificate_number').prop("disabled", true);
        $('#id_document_number').prop("disabled", false);
    }
});

$(".has_certificate_checkbox_modal").change(function () {
    let form_id = $(this).closest('form').attr('id')
    if (this.checked) {
        $(`#id_certificate_number_modal_${form_id}`).prop("disabled", false);
        $(`#id_document_number_modal_${form_id}`).prop("disabled", true);

    } else {
        $(`#id_certificate_number_modal_${form_id}`).prop("disabled", true);
        $(`#id_document_number_modal_${form_id}`).prop("disabled", false);
    }
});
