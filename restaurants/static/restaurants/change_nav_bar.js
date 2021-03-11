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
            document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:initial; color:var(--Orange);'
        }            
    } else {
        document.querySelector('nav').className = "";
        document.querySelector('.whitelogo').style.display = 'block';
        document.querySelector('.orangelogo').style.display = 'none';
        if (!document.querySelector('.sidebar-and-cards-container') && !document.querySelector('.about-container') ) { // if on profile page
            document.querySelector('.nav-links li:nth-of-type(2) a').style.cssText = 'text-decoration:underline; color:white;'
        }        
    }
}