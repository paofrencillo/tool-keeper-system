var item_count = 0;
var tools_list = []

function getTools(element) {
    let tool_is_selected = element.getAttribute("data-is-selected");
    if ( tool_is_selected == 'yes' ) return;

    let tool_id = element.id;
    let tool_name = element.getAttribute('data-tool-name');
    element.setAttribute("data-is-selected", "yes");
    element.style.border = "2px solid #a74049"
    let canvas = document.getElementById('tool-selected');
    canvas.innerHTML += `<div data-toolid="${tool_id}" class="selected-tools-wrapper mb-3 py-1">
                        <div class="d-flex">
                        <input type="text" class="selected-tools" name="${tool_id}" value="${tool_id}" readonly disabled>
                        <p class="tool_name d-flex align-items-center">${tool_name}</p>
                        </div> 
                        <div class="remove-btn" onclick="removeSelectedTool(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                        </div>
                        </div>`;
    item_count += 1;
    
    if ( item_count != 0 ) {
        document.getElementById('options').style.display = "block";
    }
}

function removeSelectedTool(element) {
    let tool_id = element.parentNode.getAttribute('data-toolid');
    element.parentNode.remove();
    document.getElementById(tool_id).style.border= "2px solid #207A29";
    document.getElementById(tool_id).setAttribute("data-is-selected", "no");
    item_count -= 1;

    if ( item_count == 0 ) {
        document.getElementById('options').style.display = "none";
    }
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

    if ( item_count == 0 ) {
        document.getElementById('options').style.display = "none";
    }
}

// Filter Tools
function filter() {
    let storage = document.getElementById('storage').value;
    let layer = document.getElementById('layer').value;
    let tools = document.getElementsByClassName('card');

    for ( i=0; i<tools.length; i++ ) {
        tools[i].style.display = 'flex';
    }

    if ( storage != '0' ) {
        if ( layer != '0' ) {
            
            for ( i=0; i<tools.length; i++ ) {
                console.log(tools[i]);
                
                if ( tools[i].getAttribute('data-storage') != storage ) {
                    tools[i].style.display = 'none';
                    continue
                }

                if ( tools[i].getAttribute('data-layer') != layer ) {
                    tools[i].style.display = 'none';
                }         
            }
        }
    }
}

// Submit post on submit
$('#tool-selected-form').on('submit', function(event){
    event.preventDefault();
    selected_tools = document.getElementsByClassName('selected-tools');
    
    for ( i=0; i<selected_tools.length; i++ ) {
        tools_list.push(parseInt(selected_tools[i].value));
    }
    document.getElementById('selected-tools-all').value = tools_list;
    $(this).unbind('submit').submit();
});

// show modal when reservation success
$(document).ready(function(){
    let show_modal = document.getElementById('show_modal').getAttribute('data-show-modal');
    if ( show_modal == 'true' ) {
        $("#modal").modal('show');
    }
});

var headers = document.getElementsByTagName("h6");

for (let i = 0; i < headers.length; i++) {
    if (headers[i].textContent == "AVAILABLE") {
        headers[i].style.color = "green";
    }
    else if (headers[i].textContent== "NOT AVAILABLE") {
        headers[i].style.color = "red";
    }
}
