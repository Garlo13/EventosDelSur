/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
var latitud, longitud, nombreEvento, tags;
var tagMalaga = ['Malaga'];
window.flickrTags= !window.flickrTags.length ==0 ? window.flickrTags : tagMalaga;


var xhttp;
xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = handleResponse;

var API_KEY = "ce467785e4e6b7dc282e86e0f2268c26";
var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search" +
        "&format=json&api_key=" + API_KEY + "&tags=" + window.flickrTags;

xhttp.open("GET", url, true);
xhttp.send(null);

$(document).ready(function () {

	latitud = window.geolocalizacion[0];
	longitud = window.geolocalizacion[1];
	nombreEvento = window.nombreEvento[0];
    initMap();

});

function initMap() {
    var map = new google.maps.Map(document.getElementById('map-canvas'), {
        center: new google.maps.LatLng(latitud, longitud),
        zoom: 15,
        draggable: true
    });
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitud, longitud),
        map: map,
        animation: google.maps.Animation.DROP,
        title: nombreEvento
    });

    var infowindow = new google.maps.InfoWindow({
        content: nombreEvento
    });
    // Adding a click event to the marker
    google.maps.event.addListener(marker, 'click', function () {
        // Calling the open method of the infoWindow
        infowindow.open(map, marker);
    });
}
;

function handleResponse() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {

        var response = xhttp.responseText;
        var substring = "jsonFlickrApi";
        var idx = response.indexOf(substring);
        var response = response.substring(idx + substring.length + 1, response.length - 1);
        var texto = JSON.parse(response);
        console.log(texto);
        var fotos = texto.photos.photo;
        urlimg = 'http://farmFARM.staticflickr.com/SERVER/ID_SECRET_SIZE.jpg';
        var elem;
        var urlimg;
        var FARM;
        var SERVER;
        var ID;
        var SECRET;
        var SIZE = 'z';
        var i = 0;

        while (i < 3) {
            elem = document.createElement('img');
            FARM = fotos[i].farm;
            SERVER = fotos[i].server;
            ID = fotos[i].id;
            SECRET = fotos[i].secret;
            urlimg = 'http://farm' + FARM + '.staticflickr.com/' + SERVER + '/' + ID + '_' + SECRET + '_' + SIZE + '.jpg';
            elem.src = urlimg;
            document.getElementById("foto" + i).appendChild(elem);

            i++;
        }
    }
}
