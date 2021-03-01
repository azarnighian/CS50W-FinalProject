document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(function (button) {
        // https://stackoverflow.com/questions/24050456/onclick-assigned-function-with-parameters            
        button.addEventListener('click', addOrRemove);
    });
});    

// Add or remove restaurant from user's list
function addOrRemove() {        
    let buttons_parent = this.parentElement;
    let info = buttons_parent.querySelector('.invisible_info');

    regular_id = info.querySelectorAll('li')[0].innerHTML;
    details_id = info.querySelectorAll('li')[1].innerHTML;
    
    let current_status = this.innerHTML;

    if (current_status === "Add to saved restaurants") {
        fetch(`/add_or_remove/add/${regular_id}/${details_id}`);        
        this.innerHTML = "Remove from saved restuarants";        
    }
    else {
        fetch(`/add_or_remove/remove/${regular_id}/${details_id}`);        
        this.innerHTML = "Add to saved restaurants";        
    }    
}
