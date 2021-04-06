document.addEventListener('DOMContentLoaded', function () {
    // https://www.w3schools.com/howto/howto_css_modals.asp

    var modal = document.querySelector('.modal');
    var closeButton = document.querySelector('.close');

    closeButton.onclick = function () {
        modal.style.display = "none";
    }    
});