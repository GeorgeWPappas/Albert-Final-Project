function uploadImage() {
    alert('image uploaded')

    // FAILED
    // var form = document.createElement("form"); 
    // alert('test1')
    // form.setAttribute("method", "post"); 
    // alert('test2')
    // form.setAttribute("action", "https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g=="); 
    // alert('test3')
    // form.setAttribute("enctype", "multipart/form-data");
    // alert('test4')
    // form.setAttribute("target", "_blank");

    // var i = document.createElement("input"); //input element, text
    // i.setAttribute('type',"file");
    // i.setAttribute('name',"filename");  

    // var s = document.createElement("input"); //input element, Submit button
    // s.setAttribute('type',"submit");
    // s.setAttribute('value',"Submit");

    // form.appendChild(i);
    // form.appendChild(s);

    // document.getElementsByTagName('body')[0].appendChild(form);

    // alert(form.value)
}

function printEXIF() {
    alert('printing info')

    //FAILED 
    // document.forms[filename].action='action="https://albert-upload-image.azurewebsites.net/api/Upload-User-Image?code=y6cWO/8xzFfJqBXgg47QTMmm2iK/xJ37pV68xVhIaBxpvhDT9J536g=="';
    // document.forms[filename].method='POST';
    // document.forms[filename].target='_blank';
    // document.forms[filename].enctype="multipart/form-data";
    // document.forms[filename].submit();

    // alert(filename.value)



    //FAILED
    // var txt = 'https://albert-final-project-function.azurewebsites.net/api/gps_extractor?'
    // var obj = JSON.parse(txt);

    // alert(obj);

    // document.getElementById("date").innerHTML = obj.date;
    // document.getElementById("latitude").innerHTML = obj.latRef + " " + obj.lat;
    // document.getElementById("longitude").innerHTML = obj.lonRef + " " + obj.lon;
    // document.getElementById("altitude").innerHTML = obj.alt;
}

// add random marker to map for testing purposes
function showMarker() {
    
    var lat = Math.floor(Math.random()*90) + 1;
    var lon = Math.floor(Math.random()*180) + 1;

    var myLatLon = new google.maps.LatLng(lat, lon)

    var mapOptions = {
        zoom: 4,
        center: myLatLon
    }   

    var map = new google.maps.Map(document.getElementById("map"), mapOptions)

    var marker = new google.maps.Marker ({
        position: myLatLon,
        title: "Image Location"
    });

    marker.setMap(map)
}

function doall() {
    uploadImage()

    printEXIF()

    showMarker()
}