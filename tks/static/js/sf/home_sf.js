var toolSelected = document.getElementById('tool-quantity');
var item_count = 0;
var tools_list = []

function getTools(element) {
    let tool_is_selected = element.childNodes[1].getAttribute("data-is-selected");
    if ( tool_is_selected == 'yes' ) return;

    let tool_id = element.id;
    element.childNodes[1].setAttribute("data-is-selected", "yes");
    element.childNodes[1].style.border = "2px solid #a74049"
    let canvas = document.getElementById('tool-selected');
    canvas.innerHTML += `<div data-toolid="${tool_id}" class="selected-tools-wrapper input-group align-items-center mb-3 py-1">
                        <input type="text" class="form-control selected-tools" name="${tool_id}" value="${tool_id}" readonly disabled>
                        <div class="remove-btn" onclick="removeSelectedTool(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                        </div>
                        </div>`;
    item_count += 1;
    toolSelected.innerHTML = item_count;
}

function removeSelectedTool(element) {
    let tool_id = element.parentNode.getAttribute('data-toolid');
    element.parentNode.remove();
    document.getElementById(tool_id).childNodes[1].style.border= "2px solid #207A29";
    document.getElementById(tool_id).childNodes[1].setAttribute("data-is-selected", "no");
    item_count -= 1;
    toolSelected.innerHTML = item_count;
}

function removeAllSelectedTools() {
    let canvas = document.getElementById('tool-selected');
    let cards = document.getElementsByClassName('card')
    let child = canvas.firstElementChild;
    while ( child ) {
        canvas.removeChild(child);
        child = canvas.firstElementChild;
    }

    for ( let i=0; i<cards.length; i++ ) {
        cards[i].style.border = "2px solid #207A29";
        cards[i].setAttribute('data-is-selected', 'no');
    }

    item_count = 0;
    toolSelected.innerHTML = item_count;
}

// Submit post on submit
$('#tool-selected-form').on('submit', function(event){
    event.preventDefault();
    selected_tools = document.getElementsByClassName('selected-tools');
    
    for ( i=0; i<selected_tools.length; i++ ) {
        tools_list.push(parseInt(selected_tools[i].value));
    }
    document.getElementsByName('selected-tools-all')[0].value = tools_list;
    console.log(document.getElementsByName('selected-tools-all')[0])
    $(this).unbind('submit').submit();
    // let fd = new FormData();

    // let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    // fd.append('csrfmiddlewaretoken', csrf)

    // let selected_tools = document.getElementsByClassName('selected-tools');
    
    // for ( i=0; i<selected_tools.length; i++ ) {
    //     fd.append(selected_tools[i].name , selected_tools[i].value);
    // }

    // let url = document.getElementById('tool-selected-form').getAttribute('data-url')
    
    // $.ajax({
    //     url : url, // the endpoint
    //     type : "POST", // http method
    //     data : fd, // data sent with the post request

    //     // handle a successful response
    //     success : function(response) {
    //         document.html; // another sanity check
    //     },

    //     // handle a non-successful response
    //     error : function(err) {
    //         console.log(err)
    //     },

    //     cache: false,
    //     contentType: false,
    //     processData: false,
    // });
});