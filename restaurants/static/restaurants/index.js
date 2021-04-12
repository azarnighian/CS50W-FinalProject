document.addEventListener('DOMContentLoaded', function () {
    // https://cs50.harvard.edu/web/2020/notes/5/#local-storage
    // https://stackoverflow.com/questions/24189428/display-a-popup-only-once-per-user
    if (localStorage.getItem('popupState') != 'shown') {
        // https://www.w3schools.com/howto/howto_css_modals.asp

        var modal = document.querySelector('.modal');
        var closeButton = document.querySelector('.close');

        // Show the modal
        modal.style.display = "flex";

        // Remove the modal after clicking the close button
        closeButton.addEventListener('click', function () {
            modal.style.display = "none";
        });
        
        localStorage.setItem('popupState', 'shown');
    }            
});