$(window).on('load', ()=> {
    var status = document.getElementById('status');
    status.style.fontWeight = 'bold';

    if (status.innerText == 'RESERVED') {
        status.style.color = '#9C9C06';
    } else if (status.innerText == 'BORROWED') {
        status.style.color = '#008000';
    } else if (status.innerText == 'RETURNED') {
        status.style.color = '#0000FF';
    }  
});

// $(window).on('load', ()=> {
//     let borrow_datetime_str = document.getElementById('borrow-datetime').innerText;
//     let return_datetime_str = document.getElementById('return-datetime').innerText;
//     let borrow_datetime = new Date(borrow_datetime_str);
//     let return_datetime = Date.parse(return_datetime_str);
//     let datetime_now = new Date();

//     let url = decodeURI("{% url 'check_datetime_tk' details.id %}")
//     $.ajax({
//       type: "GET",
//       url: url,
//       dataType: "json",
//       success: (response)=> {
//         let datetimes = JSON.parse(response.datetimes);
//         console.log(datetimes);

//       },
//       error: ()=> {
//           alert("pota");
//       }
//     });


//     // if ( datetime_now <= borrow_datetime ) {
//     //     alert("yes");
//     // } else {
//     //     alert("supot");
//     // }
// });