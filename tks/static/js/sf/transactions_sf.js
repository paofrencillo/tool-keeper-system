$(document).ready(()=> {
    let status = document.getElementsByClassName('status');

    for ( let i=0; i<status.length; i++ ) {
        let status_data = status[i].getAttribute('data-status');
        
        if ( status_data == 'RESERVED' ) {
            status[i].style.color = '#9C9C06';
        } else if ( status_data == 'BORROWED' ) {
            status[i].style.color = '#008000';
        } else if ( status_data == 'RETURNED' ) {
            status[i].style.color = '#0000FF';
        } else if ( status_data == 'VOIDED' ) {
            status[i].style.color = '#FF0000';
        }

        status[i].style.fontWeight = '600';
    } 
});

$('#transactions-table').DataTable( {
    "paging": true,
    "searching": true
  });