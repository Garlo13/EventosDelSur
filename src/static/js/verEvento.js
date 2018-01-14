/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
var latitud, longitud, nombreEvento, tags;
var retrievedObject = localStorage.getItem('evento');
console.log('retrievedObject: ', JSON.parse(retrievedObject));

var jsonEvento = JSON.parse(retrievedObject);

//nombreEvento = jsonEvento.nombre;

//tags = jsonEvento.tags;
console.log(window.flickrTags);

//latitud = parseFloat(jsonEvento.latitud);
//longitud = parseFloat(jsonEvento.longitud);

var xhttp;
xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = handleResponse;
//var lugar = document.getElementById("lugarid").value;
var API_KEY = "ce467785e4e6b7dc282e86e0f2268c26";
var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search" +
        "&format=json&api_key=" + API_KEY + "&tags=" + window.flickrTags;
console.log(url);
xhttp.open("GET", url, true);
xhttp.send(null);

$(document).ready(function () {
	/*
    document.getElementById('nombreEvento').innerHTML = nombreEvento;
    document.getElementById('descripcionEvento').innerHTML = jsonEvento.descripcion;
    document.getElementById('fechaInicio').innerHTML = jsonEvento.fechainicio;
    document.getElementById('fechaFin').innerHTML = jsonEvento.fechafin;
    document.getElementById('direccionEvento').innerHTML = jsonEvento.direccion;

    buscarComentariosDeEvento();
	*/
	
	latitud = window.geolocalizacion[0];
	longitud = window.geolocalizacion[1];
	console.log(window.flickrTags);
	
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
        //for (var i = 0; i < fotos.length; i++) {
        while (i < 3) {
            elem = document.createElement('img');
            FARM = fotos[i].farm;
            SERVER = fotos[i].server;
            ID = fotos[i].id;
            SECRET = fotos[i].secret;
            urlimg = 'http://farm' + FARM + '.staticflickr.com/' + SERVER + '/' + ID + '_' + SECRET + '_' + SIZE + '.jpg';
            elem.src = urlimg;
            document.getElementById("foto" + i).appendChild(elem);
            //document.body.appendChild(elem);
            i++;
        }
    }
}

function enviarComentario() {
    console.log('Envio comentario');
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8080/AgendaSurServerREST/webresources/agendasur.entity.comentario',
        contentType: 'application/json',
        dataType: "json", // data type of response
        data: textareaToJSON(),
        success: function (response) {
            buscarComentariosDeEvento();
            $('#comentarioTextarea').val('');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('Usted ya ha escrito una valoración.');
        }
    });
}

function textareaToJSON() {
    var date = new Date();
    return JSON.stringify({
        "apellidosCreador": localStorage.getItem('apellidoUsuario'),
        "comentario": $('#comentarioTextarea').val(),
        "comentarioPK": {
            "eventoId": jsonEvento.id,
            "usuarioEmail": localStorage.getItem('emailUsuario')
        },
        "fecha": dateParser(date),
        "nombreCreador": localStorage.getItem('nombreUsuario')
    });
}

function dateParser(date) {
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();
    var time = date.toLocaleTimeString();
    return year + '-' + month + '-' + day + ' ' + time;
}

function buscarComentariosDeEvento() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8080/AgendaSurServerREST/webresources/agendasur.entity.comentario' + '/comentario/' + jsonEvento.id,
        contentType: 'application/json',
        dataType: "json", // data type of response
        success: mostrarComentarios
    });
}

function mostrarComentarios(data) {
    var list = data == null ? [] : (data instanceof Array ? data : [data]);
    
    $('#div-comentarios p').remove();
    $.each(list, function (index, comentario) {
        var well = $('<div class="well"></div>');
        var autor = $('<p>' + comentario.nombreCreador + ' ' + comentario.apellidosCreador + '</p>');
        var fecha = $('<p>' + comentario.fecha + '</p>');
        var textoComentario = $('<p>' + comentario.comentario + '</p>');
        well.append(autor);
        well.append(fecha);
        well.append(textoComentario);
        $('#div-comentarios').append(well);
    });
}

function enviarMeGusta() {
    console.log('Envio me gusta');
    $.ajax({
        type: 'PUT',
        url: 'http://localhost:8080/AgendaSurServerREST/webresources/agendasur.entity.evento' +
                '/' + jsonEvento.id + '/' + localStorage.getItem('emailUsuario'),
        contentType: 'application/json',
        dataType: "json", // data type of response
        //data: textareaToJSON(),
        success: function (response) {
            alert('Ha dado un me gusta a este evento.');
        }
    });
}

function volver(){
    window.location = "listadoEventos.html";
}
