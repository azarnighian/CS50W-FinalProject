document.addEventListener('DOMContentLoaded', function () {
    photos_div = document.querySelector('.photos');
    photos_div.querySelectorAll('img').forEach(function (img, index) {
        // https://stackoverflow.com/questions/24050456/onclick-assigned-function-with-parameters            
        img.addEventListener('click', function() {
            openModal(); 
            currentSlide(index+1);
        });
    });

    var slideIndex = 1;
    showSlides(slideIndex);
});

// https://www.w3schools.com/howto/howto_js_lightbox.asp
// Open the Modal
function openModal() {
    document.getElementById("myModal").style.display = "flex";
    document.querySelector('nav').style.display = "none";
}

// Close the Modal
function closeModal() {
    document.getElementById("myModal").style.display = "none";
    document.querySelector('nav').style.display = "flex";
}

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }    
    slides[slideIndex - 1].style.display = "block";
}
