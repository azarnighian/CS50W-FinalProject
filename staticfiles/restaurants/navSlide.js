document.addEventListener('DOMContentLoaded', function () {    
    navSlide();
});

// Nav Bar
    // https://www.youtube.com/watch?v=gXkqy0b4M5g&t=837s
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    const darkBackground = document.querySelector('.nav-active-darken-screen');

    burger.addEventListener('click', () => {
        // Toggle Nav        
        nav.classList.toggle('nav-active');
        
        // Darken background
            // https://stackoverflow.com/questions/4866229/check-element-css-display-with-javascript
        if (window.getComputedStyle(darkBackground).display === "none") {
            darkBackground.style.display = "block";
        } else if (window.getComputedStyle(darkBackground).display === "block") {
            darkBackground.style.display = "none";
        }        
        
        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.7s ease forwards ${index / 7 + 0.3}s`;
            }
        });
        // Burger Animation
        burger.classList.toggle('toggle');
    });        
}