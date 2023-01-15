$(window).on('load', ()=> {
    let storage = $('#tool_storage').val();
    let layer = $('#tool_layer').val();
    let storage_options = $('#select_storage').children()
    let layer_options = $('#select_layer').children()

    for ( let s of storage_options ) {
        if ( s.value == storage ) {
            s.remove()
            break
        }
    }

    for ( let l of layer_options ) {
        if ( l.value == layer ) {
            l.remove()
            break
        }
    }
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            console.log(e.target.result);
            $('#image').attr("src", e.target.result);
            $('#image').hide();
            $('#image').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$("#imageUpload").change(function() {
    readURL(this);
    document.getElementById('submit_img_btn').style.display = "block";
});

$('#select_storage').on('change', ()=> {
    $('#save_location_btn').removeAttr('disabled');
});

$('#select_layer').on('change', ()=> {
    $('#save_location_btn').removeAttr('disabled');
});

$('#close_location_modal_btn').click(()=> {
    $('#move_tool_location_modal').modal('hide');
    $('#select_storage').val('0');
    $('#select_layer').val('0');
    $('#save_location_btn').attr('disabled', true);
});

function openStorageModalMaintenance() {
    $('#open_storage_maintenance_modal').css('display', 'flex');
    document.activeElement.blur() 
}

function openStorageModalRemove() {
    $('#open_storage_remove_modal').css('display', 'flex');
    document.activeElement.blur()
}

function openStorageModalAvailable() {
    $('#open_storage_available_modal').css('display', 'flex');
    document.activeElement.blur()
}

$('#rfid_scan_maintenance').focusout(()=> {
    $('#rfid_scan_maintenance').focus();
});

$('#rfid_scan_remove').focusout(()=> {
    $('#rfid_scan_remove').focus();
});

$('#rfid_scan_available').focusout(()=> {
    $('#rfid_scan_available').focus();
});

$('#green-circle-maintenance').on('click', ()=> {
    $('#rfid_scan_maintenance').focus();
    $('.ready_scan').css('display', 'block');
    $('.ready_scan').text('READY TO SCAN!');
});

$('#green-circle-remove').on('click', ()=> {
    $('#rfid_scan_remove').focus();
    $('.ready_scan').css('display', 'block');
    $('.ready_scan').text('READY TO SCAN!');
});

$('#green-circle-available').on('click', ()=> {
    $('#rfid_scan_available').focus();
    $('.ready_scan').css('display', 'block');
    $('.ready_scan').text('READY TO SCAN!');
});

$('.rfid_scan').on('change', (e)=> {
    let rfid = e.target.value;
    let tool_id = $('.rfid_scan').attr('data-tool-id');

    if ( rfid == tool_id ) {
        $('.green-circle').css('background-color', 'green');
        $('.rfid_scan').val('');
        $('.ready_scan').text('SUCCESS!');
        $('#remove_btn').prop("disabled", false);
        $('#maintenance_btn').prop("disabled", false);
        $('#available_btn').prop("disabled", false);
    } else if ( rfid != tool_id ) {
        $('.rfid_scan').val('');
    }
});

$('#remove_btn').on('click', ()=> {
    $('#remove_form').submit();
});

$('#dont_remove_btn').on('click', ()=> {
    $('.ready_scan').css('display', 'none');
    $('#open_storage_remove_modal').css('display', 'none');
    $('.green-circle').css('background-color', '#878787');
    $('#remove_btn').prop("disabled", true);
    $('#maintenance_btn').prop("disabled", true);
    $('#available_btn').prop("disabled", true);
});

$('#maintenance_btn').on('click', ()=> {
    $('#maintenance_form').submit();
});

$('#dont_maintenance_btn').on('click', ()=> {
    $('.ready_scan').css('display', 'none');
    $('#open_storage_maintenance_modal').css('display', 'none');
    $('.green-circle').css('background-color', '#878787');
    $('#remove_btn').prop("disabled", true);
    $('#maintenance_btn').prop("disabled", true);
    $('#available_btn').prop("disabled", true);
});

$('#available_btn').on('click', ()=> {
    $('#available_form').submit();
});

$('#dont_available_btn').on('click', ()=> {
    $('.ready_scan').css('display', 'none');
    $('#open_storage_available_modal').css('display', 'none');
    $('.green-circle').css('background-color', '#878787');
    $('#remove_btn').prop("disabled", true);
    $('#maintenance_btn').prop("disabled", true);
    $('#available_btn').prop("disabled", true);
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
                console.log(response);
            }, 5500);
            console.log(response['message']);
            clearInterval(my_interval);
            console.log(response["message"])
            
        },
        error: function(err) {
            console.log(err);
        }
     });
});