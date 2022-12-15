$('#storages-table').DataTable( {
    "paging": true,
    "searching": true
});

$('.get_tool').on('click', (e)=> {
   
    // $('#get_tool_form').submit();
    document.getElementById('tool_id').value = e.target.value;
    console.log(document.getElementById('tool_id').value);
    $('#get_tool_form').submit()
});