var tools_id_data;
var count;

$('#borrowed-table').DataTable( {
    "paging": true,
    "searching": true
});


$(window).on('load', ()=> {
    let status = document.getElementById('status');
    status.style.fontWeight = 'bolder';

    if (status.innerText == 'RESERVED') {
        status.style.color = '#9C9C06';
    } else if (status.innerText == 'BORROWED') {
        status.style.color = '#008000';
    } else if (status.innerText == 'RETURNED') {
        status.style.color = '#0000FF';
    }  else if (status.innerText == 'VOIDED') {
        status.style.color = '#FF0000';
    }

    tools_id_data = document.getElementsByClassName('tools_to_scan');
    count = tools_id_data.length;
});

$('#return_btn').on('click', ()=> {
    $('#scan_rfid_tools_return').css('display', 'flex');
    $('#rfid_tag_return').focus();
});

$('#show_rfid_modal').on('click', ()=> {
    $('#message_modal').css('display', 'flex');
    $('#storages_modal').hide();
});

$('#rfid_tag_return').focusout(()=> {
    $('#rfid_tag_return').focus();
});

$('#rfid_tag_return').on('change', ()=> {
    for ( var i=0; i<tools_id_data.length; i++ ) {
        let get_tool_id = parseInt(tools_id_data[i].getAttribute('data-tool-id'));
        let rfid_tag = $('#rfid_tag_return').val();
        get_tool_id = get_tool_id.toString();
        $('.scan_rfid_tools_return').css('display', 'flex');

        if ( rfid_tag == parseInt(get_tool_id) ) {
            if ( tools_id_data[i].getAttribute('data-scanned') == "" ) {
                tools_id_data[i].children[5].firstElementChild.style.backgroundColor = "green";
                tools_id_data[i].setAttribute('data-scanned', 'YES');
                card_parent = document.getElementById(`row${get_tool_id}`).querySelectorAll('.form-check-input');
            }
        }
    } 
    $('#rfid_tag_return').val('');
});

$('.storage_btn').click(function(){
    var storage = $(this).attr("data-storage");
    $.ajax(
    {
        type:"GET",
        url: "/openStorage",
        data:{
                "storage": storage
        },
        success: function( response ) {
            my_interval = setInterval(()=>{
                console.log(response['message']);
            }, 5500);
            clearInterval(my_interval);         
        },
        error: function(err) {
            console.log(err);
        }
     });
});