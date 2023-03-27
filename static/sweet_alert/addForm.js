function submitForm(form) {
    Swal.fire({
        title: 'Kiritishga aminmisiz?',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Kiritish',
        denyButtonText: `Bekor qilish`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            Swal.fire('Kiritildi!', '', 'success')
            form.submit();
        } else if (result.isDenied) {
            Swal.fire('Kiritilmadi!', '', 'info')
        }
    })
    return false;
};