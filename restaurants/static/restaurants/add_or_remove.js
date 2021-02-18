// To add or remove a restaurant from the user's list of saved restaurants

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(function (button) {
        button.onclick = addOrRemove;
    });
});

function addOrRemove() {    
    let buttons_parent = this.parentElement;
    let info = buttons_parent.querySelector('.invisible_info');
    console.log(info);

    let current_status = this.innerHTML;

    if (current_status === "Add to saved restaurants") {
        this.innerHTML = "Remove from saved restuarants";
    }
    else {
        this.innerHTML = "Add to saved restaurants";
    }    

    // fetch(`/sections/${section}`)
    //     .then(response => response.text())
    //     .then(text => {
    //         // Log text and display on page
    //         console.log(text);
    //         document.querySelector('#content').innerHTML = text;
    //     });
}