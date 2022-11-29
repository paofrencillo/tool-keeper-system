function getid() {
    let input_tags = document.getElementById('profile-form').getElementsByTagName("input");

    for ( let i=0; i < input_tags.length; i++ ) {
        if (i != 3 && i != 4) {
            input_tags[i].removeAttribute('readonly', '');
        }
                    
    }
}

