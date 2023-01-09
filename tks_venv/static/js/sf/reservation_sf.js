$(window).on('load', ()=> {
    let date = new Date().toISOString().slice(0, 10);
    $('#borrow-date').attr('min', date);
    $('#return-date').attr('min', date);
});

$("#submit-btn").click(function() {
    let borrow_date = document.getElementsByName('borrow-date')[0];
    let borrow_time = document.getElementsByName('borrow-time')[0];
    let return_date = document.getElementsByName('return-date')[0];
    let return_time = document.getElementsByName('return-time')[0];

    let startTime = new Date(`${borrow_date.value} ${borrow_time.value}`);
    let endTime = new Date(`${return_date.value} ${return_time.value}`);

    if ( startTime == "Invalid Date" && endTime == "Invalid Date" ) {
        alert("Borrow and Return DateTime needed.");
        return
    } if ( startTime >= endTime ) {
        alert("Return Date and Time should be sooner than Borrow Date and Time.");
        return_date.value = null;
        return_time.value = null;  
        return
    } else {
        $("#modal1").modal('show');
    }
});

$("#reset-btn").click(function() {
    $("#modal2").modal('show');
});