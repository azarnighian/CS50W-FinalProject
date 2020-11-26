// Sources:
    // https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple#maps_geocoding_simple-javascript
    // https://developers.google.com/maps/documentation/javascript/places

document.addEventListener('DOMContentLoaded', function () {    
    const geocoder = new google.maps.Geocoder();
    document.querySelector('form').onsubmit = function (event) {
        event.preventDefault();
        geocodeAddress(geocoder, geo_callback);
    };
});

// Geocoding
function geocodeAddress(geocoder, callback) {
    const address = document.getElementById("id_city").value;
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
        for (var i = 0; i < results.length; i++) {
            console.log(results[i]);
        }
    }
}