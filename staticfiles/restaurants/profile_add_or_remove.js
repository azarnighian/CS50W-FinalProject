document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(function (button) {
        // https://stackoverflow.com/questions/24050456/onclick-assigned-function-with-parameters            
        button.addEventListener('click', removeCard);
    });
});

// Remove restaurant card from page
// Learned from here: https://cs50.harvard.edu/web/2020/notes/6/#animation
function removeCard() {
    let buttons_card = this.parentElement.parentElement;
    buttons_card.style.animationPlayState = 'running';
    buttons_card.addEventListener('animationend', () => {
        buttons_card.remove();
    })
}
