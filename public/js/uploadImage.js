// DECIDED AGAINST USING 2 BUTTONS INSTEAD
// function uploadImage() {

//     var input = document.querySelector('input[type="file"]')
//     alert(input.value)

//     var data = new FormData()
//     data.append('file', input.files[0])
//     // data.append('user', 'hubot')
//     fetch('https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g==', {
//         method: 'POST',
//         body: data,
//     }).then(
//         response => response.json(), // if the response is a JSON object
//     ).then(
//         success => alert(success), // Handle the success response object
//     ).catch(
//         error => alert(error), // Handle the error response object  
//     );




//     // // Select your input type file and store it in a variable
//     // const input = document.getElementById('filename');
    
//     // // This will upload the file after having read it
//     // const upload = (file) => {
//     //     fetch('https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g==', { // Your POST endpoint
//     //         method: 'POST',
//     //         body: file // This is your file object
//     //     }).then(
//     //         alert('hi'),
//     //         response => response.json() // if the response is a JSON object
//     //     ).then(
//     //         alert('image uploaded'),
//     //         success => console.log(success) // Handle the success response object
//     //     ).catch(
//     //         alert('failed'),
//     //         error => console.log(error) // Handle the error response object 
//     //     );
//     // };
//     // // Event handler executed when a file is selected
//     // const onSelectFile = () => upload(input.files[0]);

//     // // Add a listener on your input
//     // // It will be triggered when a file will be selected
//     // input.addEventListener('change', onSelectFile, false);


//     // FAILED
//     // var form = document.createElement("form"); 
//     // alert('test1')
//     // form.setAttribute("method", "post"); 
//     // alert('test2')
//     // form.setAttribute("action", "https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g=="); 
//     // alert('test3')
//     // form.setAttribute("enctype", "multipart/form-data");
//     // alert('test4')
//     // form.setAttribute("target", "_blank");

//     // var i = document.createElement("input"); //input element, text
//     // i.setAttribute('type',"file");
//     // i.setAttribute('name',"filename");  

//     // var s = document.createElement("input"); //input element, Submit button
//     // s.setAttribute('type',"submit");
//     // s.setAttribute('value',"Submit");

//     // form.appendChild(i);
//     // form.appendChild(s);

//     // document.getElementsByTagName('body')[0].appendChild(form);

//     // alert(form.value)
// }

async function printEXIF() {

    //FAILED 
    // document.forms[filename].action='action="https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g=="';
    // document.forms[filename].method='POST';
    // document.forms[filename].target='_blank';
    // document.forms[filename].enctype="multipart/form-data";
    // document.forms[filename].submit();
    // alert(filename.value)

    // input = document.getElementById('filename').value;
    file = await getFileName()

    
    const data = 'https://albert-final-project-function.azurewebsites.net/api/gps_extractor?path=albertprojectstorage.blob.core.windows.net/user-image&imagename=' + file
    
    obj = await getData(data);
    
    document.getElementById("date").value = obj.dateTime;
    document.getElementById("latitude").value = obj.lat + "  " + obj.latRef;
    document.getElementById("longitude").value = obj.lon + "  " + obj.lonRef;
    document.getElementById("altitude").value = obj.alt;

    return obj;
}


async function getData(data) {
    const response = await fetch(data)
    const results = await response.json()
    
    return results
}

async function getFileName() {
    var fullPath = document.getElementById('filename').value;
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        filename = filename.substring(1);
        }
    }
    return filename
}

async function showMarker(myObj) {
    
    lat1 = myObj.lat
    lon1 = myObj.lon


    var lat = parseFloat(lat1)
    var lon = parseFloat(lon1)


    // add random marker to map for testing purposes
    // var lat = Math.floor(Math.random()*90) + 1;
    // var lon = Math.floor(Math.random()*180) + 1;

    // Adds coordinates to map and places pin if data exists.
    if (latStr == 'No LAT Data') {
        // alert('MAP RESET: no latitude and longitude to map.')    // TODO: might be too much. should just display information.

        var myLatLon = await new google.maps.LatLng(41.605540, -88.077220)

        var mapOptions = {
            zoom: 8,
            center: myLatLon
        }

        var map = await new google.maps.Map(document.getElementById("map"), mapOptions)
    } else {
        var myLatLon = await new google.maps.LatLng(lat, lon)

        var mapOptions = {
            zoom: 16,
            center: myLatLon
        }   

        var map = await new google.maps.Map(document.getElementById("map"), mapOptions)

        var marker = new google.maps.Marker ({
            position: myLatLon,
            title: "Image Location"
        });

        marker.setMap(map)
    }
    //map.setZoom(map.getZoom());
    // google.maps.event.addDomListener(window, 'load', initialize);
}

async function doall() {
    // uploadImage()

    imageData = await printEXIF()   // Gets coordinates from azure function.
    showMarker(imageData)   // Displays marker on map.
}
