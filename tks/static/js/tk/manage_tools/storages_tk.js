$('#scan_rfid_modal').on('click', ()=> {
    $('#rfid').focus();
});

$('#scan_rfid_modal').on('shown.bs.modal', ()=> {
    $('#rfid').focus();
    $('#rfid').val('');
});

$('#rfid1').on('change', ()=> {
    $('#rfid_get_tool_form').submit();
});