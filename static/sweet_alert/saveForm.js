function submitForm(form) {
    Swal.fire({
        title: 'Saqlashga aminmisiz?',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Saqlash',
        denyButtonText: `Bekor qilish`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            Swal.fire('Saqlandi!', '', 'success')
            form.submit();
        } else if (result.isDenied) {
            Swal.fire('O\'zgarishlar saqlanmadi!', '', 'info')
        }
    })
    return false;
};