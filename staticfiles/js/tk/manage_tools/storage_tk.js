$('#storages-table').DataTable( {
    "paging": true,
    "searching": true
});

$('.get_tool').on('click', (e)=> {
    document.getElementById('tool_id').value = e.target.value;
    console.log(e.target.value)
    $('#get_tool_form').submit();
});

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