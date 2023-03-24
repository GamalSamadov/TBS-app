$('.delete').on('click', function (e) {
    e.preventDefault();
    var self = $(this);

    Swal.fire({
        title: 'O\'chirishga aminmisiz?',
        text: "O'chirgandan so'ng ortga qaytarishning iloji yo'q!",
        icon: 'warning',
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ha, aminman!',
        enyButtonText: `Bekor qilish`,

    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'O\'chirildi!',
                'Malumot yo\'q qilindi.',
                'success'
            )
            location.href = self.attr('href');

        }
    })
})