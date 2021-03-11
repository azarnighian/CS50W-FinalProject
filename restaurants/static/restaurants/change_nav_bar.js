// https://www.w3schools.com/jsref/prop_html_classname.asp
    // https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onscroll2

document.addEventListener('DOMContentLoaded', function () {
    window.onscroll = function () { changeNavBar() };    
});

function changeNavBar() {            
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        document.querySelector('nav').className += " nav-scrolled";
        document.querySelector('.whitelogo').style.display = 'none';
        document.querySelector('.orangelogo').style.display = 'block';
        if (!document.querySelector('.sidebar-and-cards-container') && !document.querySelector('.about-container') ) { // if on profile page
            // https://css-tricks.com/working-with-javascript-media-queries/
            const mediaQuery = window.matchMedia('(min-width: 768px)');

            if (mediaQuery.matches) {
                document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:initial; color:var(--Orange);'
            }
            else {
                document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:none; color:var(--Orange);'
            }
        } 
        // https://stackoverflow.com/questions/17094230/how-do-i-loop-through-children-objects-in-javascript
        var burgerLines = document.querySelector('.burger').children;
        for (var i = 0; i < burgerLines.length; i++) {
            burgerLines[i].style.backgroundColor = 'grey';
        }            
    } 
    else {
        document.querySelector('nav').className = "";
        document.querySelector('.whitelogo').style.display = 'block';
        document.querySelector('.orangelogo').style.display = 'none';
        if (!document.querySelector('.sidebar-and-cards-container') && !document.querySelector('.about-container') ) { // if on profile page
            // https://css-tricks.com/working-with-javascript-media-queries/
            const mediaQuery = window.matchMedia('(min-width: 768px)')

            if (mediaQuery.matches) {
                document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:underline; color:white;'
            }
            else {
                document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:none; color:var(--Orange);'
            }
        }   
        var burgerLines = document.querySelector('.burger').children;
        for (var i = 0; i < burgerLines.length; i++) {
            burgerLines[i].style.backgroundColor = 'white';
        }  
    }
}