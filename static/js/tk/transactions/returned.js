$('#returned-table').DataTable( {
    "paging": true,
    "searching": true
});

$(window).on('load', ()=> {
    let status = document.getElementById('status');
    status.style.fontWeight = 'bolder';
    status.style.color = '#0000FF'; 
});
