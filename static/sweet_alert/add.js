function submitForm(form) {
    Swal.fire({
        title: 'Barchasini to\'g\'ri bajarganingizga aminmisiz?',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Ha',
        denyButtonText: `Yo'q`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            Swal.fire('Bajarildi!', '', 'success')
            form.submit();
        } else if (result.isDenied) {
            Swal.fire('Bajarilmadi!', '', 'info')
        }
    })
    return false;
};