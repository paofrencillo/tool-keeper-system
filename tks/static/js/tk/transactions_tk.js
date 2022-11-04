$('#transactions-table').DataTable( {
  "paging": true,
  "searching": true
});

$(document).ready(function() {
  changeStyleStatus();
});

$('.filter-btn').click((e)=> {
  let url = e.target.getAttribute('data-url');
  $.ajax({
    type: "GET",
    url: url,
    dataType: "json",
    success: (response)=> {
      let transactions = JSON.parse(response.transactions);
      let datetimes = response.datetimes;
      let container = document.getElementById('tabledata');
      container.innerHTML = "";
      for ( let i in transactions ) {
        let transaction = transactions[i];
        container.innerHTML += 
        `<tr class="rows">
            <td>
                <a href="{% url 'view_transaction_details_tk' ${transactions[i]['pk']} %}">
                    <button class="btn btn-secondary w-100" id="${transactions[i]['pk']}">View</button>
                </a>
            </td>
            <td>${transaction['pk']}</td>
            <td>${transaction['fields']['fullname']}</td>
            <td>${transaction['fields']['borrower_id']}</td>
            <td>${datetimes[i]['borrow_datetime']}</td>
            <td>${datetimes[i]['return_datetime']}</td>
            <td class="status"><strong>${transaction['fields']['status']}</strong></td>
        </tr>`;
      }
      changeStyleStatus();
    },
    error: (error)=> {
        console.log(error);
    }
  });
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
    }
  }
}