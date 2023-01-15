$('#rfid').on('click', ()=> {
    document.getElementById('rfid_hidden').focus();
});

$('#rfid_hidden').on('focusout', ()=> {
    document.getElementById('rfid_hidden').focus();
});

$('#rfid_hidden').change(()=> {
    document.getElementById('add_tools_form').addEventListener('submit', function(e){
        return False;
    });

    let rfid = $('#rfid_hidden').val()
    $.ajax(
        {
            type:"GET",
            url: "/scan_tools",
            data:{
                    "rfid": rfid
            },
            success: function( response ) {
                if ( response["message"] != 'Not Found' ) {
                    const modal = bootstrap.Modal.getInstance(rfid_modal);
                    modal.hide();
                    alert("RFID existed. Try another RFID.")
                    rfid_hidden.value = "";

                } else if ( response["message"] == 'Not Found' ) {
                    rfid = document.getElementById('rfid');
                    rfid_hidden = document.getElementById('rfid_hidden')
                    rfid.value = "";
                    rfid.value = rfid_hidden.value;
                    rfid_hidden.value = "";
                    
                    const modal = bootstrap.Modal.getInstance(rfid_modal);
                    modal.hide();
                
                    rfid.nextElementSibling.style.backgroundColor = '#32a86d'
                }

            },
            error: function(err) {
                console.log(err);
            }
         });
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

$('#tool_form_reset').on('click', ()=> {
    location.reload();
});

function openCam() {
    $('#capture_img_wrapper').show();
    $('.cam_option_btns').first().show();
    let open_cam_btn = document.getElementById('open_cam_btn');
    open_cam_btn.addEventListener('click', function(ev) {
        ev.preventDefault();
    });
    
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');

    // access video stream from webcam
    navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
        // on success, stream it in video tag
        .then(function(stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function(err) {
            alert("An error occurred: " + err);
        });

    startbutton.addEventListener('click', function(ev) {
        ev.preventDefault();
    }, false);

    $('#open_cam_btn').hide();
}

function removepicture() {
    canvas.style.display = "none";
    video.style.display = "block";
    $('#canvas').removeAttr("width");
    $('#canvas').removeAttr("height");
    $('.cam_option_btns').first().show();
    $('.cam_option_btns').last().hide();
    $('#tool_img').removeAttr("value");
    
    openCam();
}

function takepicture() {
    $('#canvas').show();
    $('.cam_option_btns').first().hide();
    $('.cam_option_btns').last().show();
    var context = canvas.getContext('2d');
    var width = $('#video').width();
    var height = $('#video').height();
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/png');
        document.getElementById('tool_img').value = data;
        document.getElementById('add_tools_form').addEventListener('submit', function(evt){
           return true;
            });
    }

    const stream = video.srcObject;
    const tracks = stream.getTracks();

    tracks.forEach((track) => {
        track.stop();
    });

    video.srcObject = null;
    video.style.display = "none";
}

$('#hide_storages_modal').on('click', ()=> {
    $('#storages_modal').hide(); 
});

$("input[name*='tool_name']").on('change', ()=> {
    let tool_name = $("input[name*='tool_name']").val();

    $("input[name*='tool_name']").val(tool_name.toUpperCase())
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