function initMap() {
    var map = L.map('map').setView([51.505, -0.09], 13);

    var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);


    var geocoder = L.Control.geocoder({
        defaultMarkGeocode: false
    })
        .on('markgeocode', function(e) {
            map.fitBounds(e.geocode.bbox);
        })
        .addTo(map);



    // queryElement
    // $("#map").height($(window).height()).width($(window).width());
    // map.invalidateSize();



    return map
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function addMultipleMarkersToMap(data) {
    for(d of data) {
        addMarkerToMap(d['lat'], d['lng'], d['desc'], d['level'], d['username']);
    }
}

function addMarkerToMap(lat, lng, desc, level, username) {

    var marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(`<p class="danger-on-map danger-on-map-${level}">${desc}</p>
                    <p class="danger-on-map">dodane przez: ${username} </p>
            `);
}

async function getUser() {
    var response = await fetch('/api/user')
        .then((response) => response.json())

    return response['username']
}

function apiAddDanger(lat, lng) {

    var data = {
        'level': document.querySelector('input[name="danger-level"]:checked').value,
        'desc': document.querySelector('input[name="danger-description"]').value,
        'lat': lat, 'lng': lng
    }
    postData('/api/dangers', data)
    username = getUser()
    addMarkerToMap(data['lat'], data['lng'], data['desc'], data['level'], username)
    map.closePopup();
}


function apiGetDangers() {
    fetch('/api/dangers')
        .then((response) => response.json())
        .then((data) => addMultipleMarkersToMap(data));
}


function getMapPopup(lat, lng) {
    return `<p style="font-size: 14px">
        Dodaj zagrożenie:
        <input name="danger-description" type="text" /> <br />
        <label> <input name="danger-level" value="low" type="radio" /> niskie </label>
        <label> <input name="danger-level" value="medium" type="radio" /> średnie </label>
        <label> <input name="danger-level" value="high" type="radio" /> wysokie </label> <br />
        <button class="btn" onClick="apiAddDanger(${lat}, ${lng})">OK</button>
        </p>
    `
}

function onMapClick(e) {
    popup = L.popup();
    popup
        .setLatLng(e.latlng)
        .setContent(getMapPopup(e.latlng.lat, e.latlng.lng))
        .openOn(map);
}

map = initMap()
map.on('click', onMapClick);

apiGetDangers()
