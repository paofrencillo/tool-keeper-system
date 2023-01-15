var tools_length = document.querySelectorAll('.tool_wrapper_modal').length;

$(window).on('load', ()=> {
    let status = document.getElementById('status');
    status.style.fontWeight = 'bolder';
    status.style.color = '#9C9C06';
    
    let locations = document.querySelectorAll('.tool_locations');
    let storages = []

    locations.forEach(element => {
        storages.push(element.getAttribute('data-location'));
    });

    storages = [...new Set(storages)]

    let storages_btns = document.getElementById('tool_storages');
    
    storages.forEach((element) => {
        storages_btns.innerHTML += `<div class="btn btn-primary storage_btn" data-storage="${element}" onclick="openStorage(this)">Open Storage ${element}</div>`
    });
});

function openStorage(element) {
    var storage = $(element).attr("data-storage");
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
};

function rfidFocus() {
    $('#rfid').focus();
}

const borrow_modal = document.getElementById('borrow_modal')
    borrow_modal.addEventListener('hidden.bs.modal', e => {
        $('#scan_btn').css('display', 'inline-block');
        $('#borrow_btn').css('display', 'none');
        $('#scanning_btn').css('display', 'none');
})

$('#scan_btn').on('click', ()=> {
    $('#scan_btn').css('display', 'none');
    $('#borrow_btn').css('display', 'none');
    $('#scanning_btn').css('display', 'inline-block');
    // $('body').focusout()
    $('#rfid').trigger('focus');
    
});

$('#rfid').focusout(()=>{
    $('#rfid').focus();
});

$('#rfid').on('change', ()=>{
    document.getElementById('borrow_form').addEventListener('submit', (event)=>{
        event.preventDefault();
    });
    let rfid = $('#rfid').val();
    $.ajax(
        {
            type:"GET",
            url: "/scan_tools",
            data:{
                    "rfid": rfid
            },
            success: function( response ) {
                console.log(response);
                $('#rfid').val(null);

                let tools = document.querySelectorAll('.tool_wrapper_modal');

                tools.forEach((element) => {
                    if ( element.id == response["tool_name"] ) {
                        if ( element.getAttribute('data-scanned') != 'yes' ) {
                            tools_length -= 1;
               
                            if ( tools_length == 0 ) {
                                $('#scanning_btn').css('display', 'none');
                                $('#borrow_btn').css('display', 'inline-block');
                            }
                        }
                        $(`#${response["tool_name"]}_input`).val(response["tool_id"])
                        $(`#${response["tool_name"]}_scanned`).css('display', 'inline-block')
                        element.style.backgroundColor = "rgb(174, 230, 194)";
                        element.setAttribute('data-scanned', 'yes') 
                    }
                });
            },
            error: function(err) {
                console.log(err);
            }
        });
});

