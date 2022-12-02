$('#rfid').on('click', ()=> {
    document.getElementById('rfid_hidden').focus();
});

$('#rfid_hidden').change(()=> {
    rfid = document.getElementById('rfid');
    rfid_hidden = document.getElementById('rfid_hidden')
    rfid.value = "";
    rfid.value = rfid_hidden.value;
    rfid_hidden.value = "";
    
    const modal = bootstrap.Modal.getInstance(rfid_modal);
    modal.hide();

    rfid.nextElementSibling.style.backgroundColor = '#32a86d'
});

$('.tool_details').change(( event )=> {
    event.target.nextElementSibling.style.backgroundColor = '#32a86d';
});

$('#tool_details_reset').on('click', ()=> {
    green_circles = document.getElementsByClassName('green-circle');

    for ( i=0; i<green_circles.length; i++ ) {
        green_circles[i].style.backgroundColor = '#878787'
    }
});
