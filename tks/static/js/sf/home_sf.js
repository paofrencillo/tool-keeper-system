const toolSelected = document.getElementById('tool-quantity');
var item_count = 0


function getTools(element) {
    item_count += 1;
    toolSelected.innerHTML = item_count;
    var tool_id = element.getAttribute('toolid');
    var tool_name = element.childNodes[1].innerText;
    const canvas = document.getElementById('tool-selected');
    canvas.innerHTML += `<div id="tool${tool_id}Selected" class="selected-tools-wrapper input-group align-items-center mb-3 py-1">
                        <input type="text" class="form-control selected-tools" value="${tool_id + '    ' + tool_name}" readonly disabled>
                        <div id="remove${tool_id}" class="remove-btn" onclick="removeSelectedTool(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                        </div>
                        </div>`;
}

function removeSelectedTool(element) {
    element.parentNode.remove();
    item_count -= 1;
}


