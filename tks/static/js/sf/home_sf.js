

const toolSelected = document.getElementById('tool-quantity');
var item_count = 0

// document.querySelectorAll('.tools').forEach(occurence => {
//     occurence.addEventListener('click', (e) => {
//        item_count += 1;
//        toolSelected.innerHTML = item_count;
//        var tool_id = e.target.parentNode.getAttribute('toolid');
       
//        var tool_name = e.target;
//        console.log(tool_name)
//     });
// });


// const canvas = document.getElementById('tool-selected');

// document.querySelectorAll('.card').forEach(occurence => {
//     occurence.addEventListener('click', (e) => {
//        canvas.innerHTML = toolSelected.textContent;
       
//     });
// });

var tool_list = [];

function getTools(element) {
    item_count += 1;
    toolSelected.innerHTML = item_count;
    var tool_id = element.getAttribute('toolid');
    var tool_name = element.childNodes[1].innerText;
    tool_list.push(tool_name);
    const canvas = document.getElementById('tool-selected');
    for (let i = 0; i < tool_list.length; i++) {
        canvas.innerHTML += tool_list[i] + "<br>";
        }

    console.log(tool_list);
}


