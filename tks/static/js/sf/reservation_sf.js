
$("#submit-btn").click(function() {
    let borrow_date = document.getElementsByName('borrow-date')[0];
    let borrow_time = document.getElementsByName('borrow-time')[0];
    let return_date = document.getElementsByName('return-date')[0];
    let return_time = document.getElementsByName('return-time')[0];

    let startTime = new Date(`${borrow_date.value} ${borrow_time.value}`);
    let endTime = new Date(`${return_date.value} ${return_time.value}`);
    let currentTime = new Date();

    if ( startTime == "Invalid Date" && endTime == "Invalid Date" ) {
        alert("Borrow and Return DateTime needed.");
        return
    } if ( currentTime > startTime ) {
        alert("Borrow Date and Time should be sooner than Current Date and Time.");
        borrow_date.value = null;
        borrow_time.value = null;
        return_date.value = null;
        return_time.value = null;
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