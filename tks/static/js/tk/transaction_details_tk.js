var tools_id_data;
var count;

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
    
    let check_br_datetime = document.getElementById('borrow-datetime');
    let check_rt_datetime = document.getElementById('return-datetime');

    if ( check_br_datetime.getAttribute('data-check-borrow-dt') == "False" ) {
        check_br_datetime.style.color = "#FF0000";
    }
    if ( check_rt_datetime.getAttribute('data-check-return-dt') == "False" ) {
        check_rt_datetime.style.color = "#FF0000";
    }

    tools_id_data = document.getElementsByClassName('tools_to_scan');
    count = tools_id_data.length;
});

$('#message_modal_btn').on('click', ()=> {
    $('#message_modal').hide();
    $('#scan_rfid_tools').css('display', 'flex');
    $('#rfid_tag').focus();
});

$('#rfid_tag').focusout(()=> {
    $('#rfid_tag').focus();
});

$('#rfid_tag').on('change', ()=> {
    document.getElementById('borrow_form').addEventListener('submit', (event)=>{
        event.preventDefault();
    });
    for ( var i=0; i<tools_id_data.length; i++ ) {
        let get_tool_id = parseInt(tools_id_data[i].getAttribute('data-tool-id'));
        let rfid_tag = $('#rfid_tag').val();

        if ( rfid_tag == parseInt(get_tool_id) ) {
            if ( tools_id_data[i].getAttribute('data-scanned') == "" ) {
                tools_id_data[i].lastElementChild.firstElementChild.style.backgroundColor = "green";
                tools_id_data[i].setAttribute('data-scanned', 'YES');
                count -= 1;
            }

            if ( count == 0 ) {
                setTimeout(()=> {
                    $('#borrow_form').submit();
                }, 2000);   
            } 
        }
    } 
    $('#rfid_tag').val('');
});