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

// function openCam(){
//     
//     document.getElementById('open_cam_btn').style.display = 'none';
//     document.getElementsByClassName('cam_option_btns')[0].style.display = 'block';
//     document.getElementsByClassName('cam_option_btns')[1].style.display = 'block';

//     let All_mediaDevices=navigator.mediaDevices
//     if (!All_mediaDevices || !All_mediaDevices.getUserMedia) {
//        alert("getUserMedia() not supported.");
//        return;
//     }
//     All_mediaDevices.getUserMedia({
//        audio: false,
//        video: true
//     })
//     .then(function(vidStream) {
//        var video = document.getElementById('vid');
//        if ("srcObject" in video) {
//           video.srcObject = vidStream;
//        } else {
//           video.src = window.URL.createObjectURL(vidStream);
//        }
//        video.onloadedmetadata = function(e) {
//           video.play();
//        };
//        video.scrollIntoView({behavior: 'smooth'});
//     })
//     .catch(function(e) {
//        alert(e.name + ": " + e.message);
//     });
//  }

// function openCam() {
    Webcam.set({
    width: 350,
    height: 350,
    image_format: 'jpeg',
    jpeg_quality: 90
});

// document.getElementById('capture_img_wrapper').style.display = 'block';
Webcam.attach('#vid')
// }
    


