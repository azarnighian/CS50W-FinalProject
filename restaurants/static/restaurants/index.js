// Sources:
    // https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple#maps_geocoding_simple-javascript
    // https://developers.google.com/maps/documentation/javascript/places
    
    // https://www.youtube.com/watch?v=gXkqy0b4M5g&t=837s

document.addEventListener('DOMContentLoaded', function () {    
    navSlide();
    
    // const geocoder = new google.maps.Geocoder();
    // document.querySelector('form').onsubmit = function (event) {
    //     // event.preventDefault();
    //     // geocodeAddress(geocoder, geo_callback);
    //     send_to_view;
    // };
    // document.querySelector('.testing_button').onclick = tester;    
});

// Geocoding
function geocodeAddress(geocoder, callback) {
    address = document.getElementById("id_city").value;
    geocoder.geocode({ address: address }, (results, status) => {
        if (status === "OK") {
            callback(results);
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

function geo_callback(results) {
    coordinates = [results[0].geometry.location.lat(), results[0].geometry.location.lng()]
    search(coordinates);
}


// Maps Javascript API

var service;

function search(coordinates) {           
    var city = new google.maps.LatLng(coordinates[0], coordinates[1]);

    var request = {
        location: city,
        radius: '3000',
        type: ['restaurant']
    };

    service = new google.maps.places.PlacesService(document.createElement('div'));
    service.nearbySearch(request, search_callback);
}

function search_callback(results, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        send_to_view(results);
    }
}

function tester() {
    const data = { username: 'example' };

    fetch('/testing', {
        method: 'POST',        
        body: JSON.stringify(data)
    })          
}

function send_to_view(results) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const data = { username: 'example' };
    fetch(`/results/${address}`, {
        method: 'POST',
        mode: 'same-origin',
        headers: { 
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'                        
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Nav Bar
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li')

    burger.addEventListener('click', () => {
        // Toggle Nav
        nav.classList.toggle('nav-active');

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