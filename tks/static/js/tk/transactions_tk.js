$('#transactions-table').DataTable( {
  "paging": true,
  "searching": true
});

$(document).ready(function() {
  var status = document.getElementsByClassName('status');
  for ( const s of status ) {
    if ( s.innerText == 'RESERVED' ) {
      s.style.color = '#9C9C06';
    } else if ( s.innerText == 'BORROWED' ) {
      s.style.color = '#008000';
    } else if ( s.innerText == '0000FF' ) {
      s.style.color = '#9C9C06';
    }
  }
});