document.addEventListener('DOMContentLoaded', function () {    
    document.querySelector('.filters-bar').addEventListener('click', () => filters_bar());
});

function filters_bar() {
    // if (document.querySelector('.sidebar-container').style.display === 'none') {
    // https://stackoverflow.com/questions/28100979/button-does-not-function-on-the-first-click
    // https://stackoverflow.com/questions/4866229/check-element-css-display-with-javascript/4866277
    // https://www.w3schools.com/howto/howto_js_check_hidden.asp

    var sidebar_container = document.querySelector('.sidebar-container');
    if (window.getComputedStyle(sidebar_container).display === 'none') {
        document.querySelector('.sidebar-container').style.display = 'block';
        document.querySelector('.sidebar-and-cards-container').style.width = '100%';
        document.querySelector('.cards-container').style.display = 'none';
    }
    else {
        document.querySelector('.sidebar-container').style.display = 'none';
        document.querySelector('.cards-container').style.display = 'flex';
    }
}