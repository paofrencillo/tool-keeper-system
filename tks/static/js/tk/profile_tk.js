function getid() {
    let input_tags = document.getElementById('profile-form').getElementsByTagName("input");

    for ( let i=0; i < input_tags.length; i++ ) {
        if (i != 3 && i != 4) {
            input_tags[i].removeAttribute('readonly', '');
        }                   
    }
}

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
