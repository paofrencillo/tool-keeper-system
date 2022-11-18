$(document).ready(()=> {
    let status = document.getElementById('status').getAttribute('data-status');

    if ( status == 'RESERVED' ) {
        document.getElementById('status').style.color = '#9C9C06';
    } else if ( status == 'BORROWED' ) {
        document.getElementById('status').style.color = '#008000';
    } else if ( status == 'RETURNED' ) {
        document.getElementById('status').style.color = '#0000FF';
    } else if ( status == 'VOIDED' ) {
        document.getElementById('status').style.color = '#FF0000';
    }
});