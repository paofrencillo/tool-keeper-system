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

    for ( let tool of tools ) {
        tool.style.display = 'flex';
    }

    if ( storage != '0' ) {
        if ( layer != '0' ) {
            
            for ( let tool of tools ) {
                
                if ( tool.getAttribute('data-storage') != storage ) {
                    tool.style.display = 'none';
                    continue
                }

                if ( tool.getAttribute('data-layer') != layer ) {
                    tool.style.display = 'none';
                }         
            }
        }
    }
}

function resetFilter() {
    let tools = document.getElementsByClassName('card');

    for ( let tool of tools ) {
        tool.style.display = 'flex';
        document.getElementById('storage').value = "0";
        document.getElementById('layer').value = "0"; 
    }
}

// search tools
function search_tools() {
    let search = document.getElementById('search_tool').value.toLowerCase();
    let re = new RegExp(search, 'gi');
    let tools = document.getElementsByClassName('card');

    for ( let tool of tools ) { 
        let tool_name = tool.getAttribute('data-tool-name').toLowerCase();

        if ( re.test(tool_name) == true ) {
            tool.style.display = "flex";
        } else {
            tool.style.display = "none";           
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

// show colored label for availability of tools
var headers = document.getElementsByTagName("h6");

for ( let header of headers ) {
    if (header.textContent == "AVAILABLE") {
        header.style.color = "green";
    }
    else if (header.textContent== "NOT AVAILABLE") {
        header.style.color = "red";
    }
}