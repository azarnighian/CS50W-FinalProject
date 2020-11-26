// Sources:
    // https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple#maps_geocoding_simple-javascript
    // https://developers.google.com/maps/documentation/javascript/places

document.addEventListener('DOMContentLoaded', function () {    
    const geocoder = new google.maps.Geocoder();
    document.querySelector('form').onsubmit = function (event) {
        event.preventDefault();
        geocodeAddress(geocoder, callback);
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

function callback(results) {
    coordinates = [results[0].geometry.location.lat(), results[0].geometry.location.lng()]
    return coordinates;
}


// Maps Javascript API

// Get API key
// const api_key; 

// var map;
// var service;
// var infowindow;

// function search() {           
//     var pyrmont = new google.maps.LatLng(-33.8665433, 151.1956316);

//     map = new google.maps.Map(document.getElementById('map'), {
//         center: pyrmont,
//         zoom: 15
//     });

//     var request = {
//         location: pyrmont,
//         radius: '500',
//         type: ['restaurant']
//     };

//     service = new google.maps.places.PlacesService(map);
//     service.nearbySearch(request, callback);
// }

// function callback(results, status) {
//     if (status == google.maps.places.PlacesServiceStatus.OK) {
//         for (var i = 0; i < results.length; i++) {
//             createMarker(results[i]);
//         }
//     }
// }