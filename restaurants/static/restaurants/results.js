document.addEventListener('DOMContentLoaded', function () {    
    document.querySelector('.filters-bar').addEventListener('click', () => filters_bar());
});

function filters_bar() {
    if (document.querySelector('.sidebar-container').style.display === 'none') {
        document.querySelector('.sidebar-container').style.display = 'block';
        document.querySelector('.sidebar-and-cards-container').style.width = '100%';
        document.querySelector('.cards-container').style.display = 'none';
    }
    else {
        document.querySelector('.sidebar-container').style.display = 'none';
        document.querySelector('.cards-container').style.display = 'flex';
    }
}