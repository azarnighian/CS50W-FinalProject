document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(function (button) {
        updateButton(button);
    });
});
        
// Change button text to "Remove..." if restaurant is in user's list
    // Maybe do this in html if possible (see comments in results.html by the button)
function updateButton(button) {    
    let buttons_parent = button.parentElement;
    let info = buttons_parent.querySelector('.invisible_info');

    regular_id = info.querySelectorAll('li')[0].innerHTML;
    details_id = info.querySelectorAll('li')[1].innerHTML;

    // https://stackoverflow.com/questions/24050456/onclick-assigned-function-with-parameters            
    button.addEventListener('click', function () {
        addOrRemove(regular_id, details_id, button);
        console.log(regular_id);
    }); 
    
    fetch(`/check_status/${regular_id}/${details_id}`)
        .then(response => response.text())
        .then(text => {
            // if (text === "Restaurant is in my list") {
            //     button.innerHTML = "Remove from saved restuarants";
            // }
            console.log(text);
        });    
}

// Add or remove restaurant from user's list
function addOrRemove(regular_id, details_id, button) {        
    
    console.log(regular_id);
    
    let current_status = button.innerHTML;

    if (current_status === "Add to saved restaurants") {
        fetch(`/add_or_remove/add/${regular_id}/${details_id}`)        
        button.innerHTML = "Remove from saved restuarants";        
    }
    else {
        fetch(`/add_or_remove/remove/${regular_id}/${details_id}`)        
        button.innerHTML = "Add to saved restaurants";        
    }    
}
