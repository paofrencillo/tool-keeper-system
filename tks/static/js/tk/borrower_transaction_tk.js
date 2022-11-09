$(window).on('load', ()=> {
    let status = document.getElementById('status');
    status.style.fontWeight = 'bold';

    if (status.innerText == 'RESERVED') {
        status.style.color = '#9C9C06';
    } else if (status.innerText == 'BORROWED') {
        status.style.color = '#008000';
    } else if (status.innerText == 'RETURNED') {
        status.style.color = '#0000FF';
    }  

    
    let check_br_datetime = document.getElementById('borrow-datetime');
    let check_rt_datetime = document.getElementById('return-datetime');

    if ( check_br_datetime.getAttribute('data-check-borrow-dt') == "False" ) {
        check_br_datetime.style.color = "#FF0000";
    }
    if ( check_rt_datetime.getAttribute('data-check-return-dt') == "False" ) {
        check_rt_datetime.style.color = "#FF0000";
    } 
});

function checkIfVoid(datetime) {
    
}