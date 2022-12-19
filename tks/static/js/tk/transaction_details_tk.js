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

$('#message_modal_btn_return').on('click', ()=> {
    $('#message_modal_return').hide();
    $('#scan_rfid_tools_return').css('display', 'flex');
    $('#rfid_tag_return').focus();
});

$('#show_rfid_modal').on('click', ()=> {
    $('#message_modal').css('display', 'flex');
    $('#storages_modal').hide();
    
});

$('#hide_storages_modal').on('click', ()=> {
    $('#storages_modal').hide();
});

$('#rfid_tag').focusout(()=> {
    $('#rfid_tag').focus();
});

$('#rfid_tag_return').focusout(()=> {
    $('#rfid_tag_return').focus();
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
                console.log(tools_id_data[i])
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

$('#rfid_tag_return').on('change', ()=> {
    // document.getElementById('return_form').addEventListener('submit', (event)=>{
    //     event.preventDefault();
    // });
    for ( var i=0; i<tools_id_data.length; i++ ) {
        let get_tool_id = parseInt(tools_id_data[i].getAttribute('data-tool-id'));
        let rfid_tag = $('#rfid_tag_return').val();
        get_tool_id = get_tool_id.toString();
        $('.scan_rfid_tools_return').css('display', 'flex');

        if ( rfid_tag == parseInt(get_tool_id) ) {
            if ( tools_id_data[i].getAttribute('data-scanned') == "" ) {
                tools_id_data[i].children[5].firstElementChild.style.backgroundColor = "green";
                tools_id_data[i].setAttribute('data-scanned', 'YES');
                console.log(`row${get_tool_id}`);
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
            // my_interval = setInterval(()=>{
            //     console.log(response);
            // }, 5500);
            // console.log(response['message']);
            // // clearInterval(my_interval);
            console.log(response["message"])
            
        },
        error: function(err) {
            console.log(err);
        }
     });
});