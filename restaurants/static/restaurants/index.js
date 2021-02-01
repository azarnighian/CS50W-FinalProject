// Sources:
    // https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple#maps_geocoding_simple-javascript
    // https://developers.google.com/maps/documentation/javascript/places
    
    // https://www.youtube.com/watch?v=gXkqy0b4M5g&t=837s

document.addEventListener('DOMContentLoaded', function () {    
    navSlide();

    document.querySelector('.filters-bar').addEventListener('click', () => filters_bar());
    

    
    // const geocoder = new google.maps.Geocoder();
    // document.querySelector('form').onsubmit = function (event) {
    //     // event.preventDefault();
    //     // geocodeAddress(geocoder, geo_callback);
    //     send_to_view;
    // };
});


// Nav Bar
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

function filters_bar() {
    if (document.querySelector('.sidebar-container').style.display == 'none') {
        document.querySelector('.sidebar-container').style.display = 'block';
        document.querySelector('.sidebar-and-cards-container').style.width = '100%';    
        document.querySelector('.cards-container').style.display = 'none';
    }  
    else {
        document.querySelector('.sidebar-container').style.display = 'none';
        document.querySelector('.cards-container').style.display = 'flex';
    }      
}

// Geocoding
// function geocodeAddress(geocoder, callback) {
//     address = document.getElementById("id_city").value;
//     geocoder.geocode({ address: address }, (results, status) => {
//         if (status === "OK") {
//             callback(results);
//         } else {
//             alert("Geocode was not successful for the following reason: " + status);
//         }
//     });
// }

// function geo_callback(results) {
//     coordinates = [results[0].geometry.location.lat(), results[0].geometry.location.lng()]
//     search(coordinates);
// }


// // Maps Javascript API

// var service;

// function search(coordinates) {           
//     var city = new google.maps.LatLng(coordinates[0], coordinates[1]);

//     var request = {
//         location: city,
//         radius: '3000',
//         type: ['restaurant']
//     };

//     service = new google.maps.places.PlacesService(document.createElement('div'));
//     service.nearbySearch(request, search_callback);
// }

// function search_callback(results, status) {
//     if (status == google.maps.places.PlacesServiceStatus.OK) {
//         send_to_view(results);
//     }
// }

// function tester() {
//     const data = { username: 'example' };

//     fetch('/testing', {
//         method: 'POST',        
//         body: JSON.stringify(data)
//     })          
// }

// function send_to_view(results) {
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     const data = { username: 'example' };
//     fetch(`/results/${address}`, {
//         method: 'POST',
//         mode: 'same-origin',
//         headers: { 
//             'X-CSRFToken': csrftoken,
//             'Content-Type': 'application/json'                        
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Success:', data);
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     });
// }