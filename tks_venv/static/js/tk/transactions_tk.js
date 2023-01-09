$('#transactions-table').DataTable( {
  "paging": true,
  "searching": true
});

$(document).ready(function() {
  changeStyleStatus();
});

$('#transactions-table_paginate').on('click', function() {
  changeStyleStatus();
});

function changeStyleStatus() {
  var status = document.getElementsByClassName('status');
  for ( const s of status ) {
    if ( s.innerText == 'RESERVED' ) {
      s.style.color = '#9C9C06';
    } else if ( s.innerText == 'BORROWED' ) {
      s.style.color = '#008000';
    } else if ( s.innerText == 'RETURNED' ) {
      s.style.color = '#0000FF';
    } else if ( s.innerText == 'VOIDED' ) {
      s.style.color = '#FF0000';
    }
  }
}