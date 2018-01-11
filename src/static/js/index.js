
var nombre, apellidos, email;

function handleClientLoad() {
    // Loads the client library and the auth2 library together for efficiency.
    // Loading the auth2 library is optional here since `gapi.client.init` function will load
    // it if not already loaded. Loading it upfront can save one network request.
    console.log('ENTRA');
    gapi.load('client:auth2', initClient);
}

function handleConnection() {
    // Listen for sign-in state changes.
    console.log('entra 3ª');
    gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

    // Handle the initial sign-in state.
    updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
}

function initClient() {
    console.log('entra 2ªvez');
    // Initialize the client with API key and People API, and initialize OAuth with an
    // OAuth 2.0 client ID and scopes (space delimited string) to request access.
    var initialized = gapi.client.init({
        //apiKey: 'AIzaSyD-YkjNcqoEH4GND279kbs8YkW0AF5J3pg',
        discoveryDocs: ["https://people.googleapis.com/$discovery/rest?version=v1"],
        clientId: '1095663528592-3uacq2gga1bien0l9jqfh22i1o6qaf7f.apps.googleusercontent.com',
        scope: 'profile'
    });
    initialized.then(handleConnection);
}

function updateSigninStatus(isSignedIn) {
    // When signin status changes, this function is called.
    // If the signin status is changed to signedIn, we make an API call.
    console.log('entra 4ª');
    if (isSignedIn) {
        //alert('Conectado correctamente');
        console.log('entra 5ª');
        makeApiCall();
        //addUser();

    }else{
        gapi.auth2.getAuthInstance().signIn();
        
        makeApiCall();
    }
}

function handleSignInClick(event) {
    // Ideally the button should only show up after gapi.client.init finishes, so that this
    // handler won't be called before OAuth is initialized.
    gapi.auth2.getAuthInstance().signIn();
}

function handleSignOutClick(event) {
    gapi.auth2.getAuthInstance().disconnect();
    window.location = "eventos.html";
}

function makeApiCall() {
    // Make an API call to the People API, and print the user's given name.
    console.log('YEHÀ');
    gapi.client.people.people.get({
        'resourceName': 'people/me',
        'personFields': 'emailAddresses,names'
    }).then(function (response) {
        console.log(response);
        //console.log('Hello, ' + response.result.names[0].givenName);
        nombre = response.result.names[0].givenName;
        apellidos = response.result.names[0].familyName;
        email = response.result.emailAddresses[0].value;
        //alert('Hola, ' + response.result.names[0].givenName);
        
        var jsonUsuario = $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/AgendaSurServerREST/webresources/agendasur.entity.usuario/' + email,
            dataType: "json",
            success: setUsuarioSesion,
            error: addUser
        });


        //comprobamos tipo usuario

        console.log(response);
        window.location = "listadoEventos.html";
    }, function (reason) {
        console.log('Error: ' + reason.result.error.message);
    });
}

function setUsuarioSesion(data) {   
    localStorage.setItem("usuarioSesion",JSON.stringify(data));

}

/*
function addUser() {
    console.log(nombre);
    console.log(apellidos);
    console.log(email);
    console.log('hola');
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: 'http://localhost:8080/AgendaSurServerREST/webresources/agendasur.entity.usuario',
        dataType: "json",
        data: JSON.stringify({
            "nombre": nombre,
            "apellidos": apellidos,
            "email": email
        }),success: setUsuarioSesion
        
    });
}
/*