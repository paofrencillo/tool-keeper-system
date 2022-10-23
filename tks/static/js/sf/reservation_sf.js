function checkDateTime() {
    var borrow_date = document.getElementsByName('borrow-date')[0].value;
    var borrow_time = document.getElementsByName('borrow-time')[0].value;
    var return_date = document.getElementsByName('return-date')[0].value;
    var return_time = document.getElementsByName('return-time')[0].value;
    var submit_btn = document.getElementById('submit-btn');

    var startTime = new Date(`${borrow_date} ${borrow_time}`);
    var endTime = new Date(`${return_date} ${return_time}`);

    if ( startTime >= endTime ) {
        submit_btn.setAttribute("disabled", true);
        alert("start time is lesser");
    } else if ( startTime < endTime ) {
        submit_btn.removeAttribute("disabled");
    }
}

$("#submit-btn").click(function() {
    $("#modal").modal('show');
});