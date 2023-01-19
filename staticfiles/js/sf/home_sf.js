var item_count = 0;
var tools_list = []

var tool_quantity = {}

function getTools(element) {
    if ( $(element).parent().attr('selected') == 'selected' ) return;

    $(element).parent().attr('selected', 'selected')
    $(element).parent().css('border-color', 'green');
    $(element).css('background-color', 'green');

    let canvas = document.getElementById('tool-selected');
    let tool_name = $(element).parent().attr('id');
    canvas.innerHTML += `<div class="selected-tools-wrapper mb-3 py-1" data-tool-name="${tool_name}">
                        <div class="d-flex">
                        <input type="text" class="selected-tools" name="${tool_name}" value="${tool_name}" readonly disabled>
                        </div> 
                        <div class="remove-btn" onclick="removeSelectedTool(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                        </div>
                        </div>`;

    tools_list.push(tool_name);
    
    if ( tools_list.length != 0 ) {
        document.getElementById('options').style.display = "block";
    }
}

function removeSelectedTool(element) {
    let tool = element.parentNode.getAttribute('data-tool-name');
    $(`#${tool}`).removeAttr('selected');
    element.parentNode.remove();
    document.getElementById(tool).style.borderColor= "#b12323";
    document.getElementById('carousel-description-'+tool).style.backgroundColor= "#b12323";
    tools_list.pop(tool);

    if ( tools_list.length == 0 ) {
        document.getElementById('options').style.display = "none";
    }
}

function removeAllSelectedTools() {
    let canvas = document.getElementById('tool-selected');
    let carousels = document.querySelectorAll('.carousel-wrapper');
    let child = canvas.firstElementChild;

    while ( child ) {
        canvas.removeChild(child);
        child = canvas.firstElementChild;
    }

    carousels.forEach(carousel => {
        carousel.style.borderColor = "#b12323"
        document.getElementById('carousel-description-'+carousel.id).style.backgroundColor= "#b12323";
        carousel.removeAttribute('selected');
    });

    tools_list = [];

    if ( tools_list.length == 0 ) {
        document.getElementById('options').style.display = "none";
    } 
}

function resetFilter() {
    let tools = document.getElementsByClassName('carousel');

    for ( let tool of tools ) {
        tool.parentNode.style.display = 'block';
    }

    $('#search_tool').val(null);
}

// search tools
function search_tools() {
    let search = document.getElementById('search_tool').value.toLowerCase();
    let re = new RegExp(search, 'gi');
    let tools = document.getElementsByClassName('carousel-wrapper');

    for ( let tool of tools ) { 
        let tool_name = tool.getAttribute('id').toLowerCase();

        if ( re.test(tool_name) == true ) {
            tool.style.display = "block";
        } else {
            tool.style.display = "none";           
        }
    }
}

$('#search_tool').on('keyup', ()=> {
    search_tools();
});

// Submit post on submit
$('#tool-selected-form').on('submit', function(event){
    event.preventDefault();
    selected_tools = document.getElementsByClassName('selected-tools');
    
    document.getElementById('selected-tools-all').value = tools_list;
    console.log(tools_list)
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

$(window).on('load', ()=> {
    let indicators = document.querySelectorAll('.carousel-indicators');
    
    indicators.forEach(indicator => {
        indicator.firstElementChild.setAttribute('class', 'active');
        indicator.firstElementChild.setAttribute('aria-current', 'true');
    });
})
