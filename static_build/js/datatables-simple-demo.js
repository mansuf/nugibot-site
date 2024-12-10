const datatablesSimple = document.getElementById('datatablesSimple');
if (datatablesSimple) {
    new simpleDatatables.DataTable(datatablesSimple, {
        sortable: false, // Nonaktifkan sorting
        perPage: 5,       // Tampilkan 5 entri per halaman secara default
        perPageSelect: false
    });
}
