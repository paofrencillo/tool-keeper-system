function getid() {
    let input_tags = document.getElementById('profile-form').getElementsByTagName("input");

    for ( let i=0; i < input_tags.length; i++ ) {
        input_tags[i].removeAttribute('readonly', '');               
    }
}