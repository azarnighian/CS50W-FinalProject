// Change cursor to progress on submit

// Stopped using this because of the following issue:
    // https://stackoverflow.com/questions/1718415/getting-the-browser-cursor-from-wait-to-auto-without-the-user-moving-the-mou/37351569#37351569
    // https://stackoverflow.com/questions/36597412/mouse-cursor-set-using-jquery-css-not-changing-until-mouse-moved

document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('form');
    var submitButton = document.querySelector('input[type=submit]');

    // (For when the page reloads after filters form submission)
    // submitButton.style.cursor = 'auto';
    // document.body.style.cursor = 'auto';

    form.addEventListener('submit', function () {
        submitButton.style.cursor = 'progress';
        document.body.style.cursor = 'progress';        
    });
});