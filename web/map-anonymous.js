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



    return map
}


function addMarkerToMap(lat, lng, desc, level, username) {

    var marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(`<p class="danger-on-map danger-on-map-${level}">${desc}</p>
                    <p class="danger-on-map">dodane przez: ${username} </p>
            `);
}


function addMultipleMarkersToMap(data) {
    for(d of data) {
        addMarkerToMap(d['lat'], d['lng'], d['desc'], d['level'], d['username']);
    }
}


function apiGetDangers() {
    fetch('/api/dangers')
        .then((response) => response.json())
        .then((data) => addMultipleMarkersToMap(data));
}


function getMapPopup(lat, lng) {
    return `<p style="font-size: 14px">
        Aby dodać zagrożenie, musisz się zalogować <a href="/login">zaloguj</a>
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
