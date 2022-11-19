function getid() {
    let input_tags = document.getElementById('profile-form').getElementsByTagName("input");

    for ( let i=2; i < input_tags.length - 2; i++ ) {
        input_tags[i].removeAttribute('readonly', '');               
    }
}