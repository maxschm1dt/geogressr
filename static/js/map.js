var map = L.map('map').setView([38.0, -20.0], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var markersLayer = L.layerGroup().addTo(map);

fetch('/get-geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: function (feature) {
                var c
                switch (feature.properties.rarity){
                    case "uncommon coverage":
                        c = '#997c68';
                        break;
                    case 'common coverage':
                        c = '#75d17b';
                        break;
                    case 'rare coverage':
                        c = '#d17ca6';
                        break;
                    default:
                        c = '#adadad';
                        break;
                }
                return {
                    color: c,
                    weight: 1,
                    fillOpacity: 0.3
                };
            },
            onEachFeature: function (feature, layer) {
                //layer.bindPopup(feature.properties.name);

                layer.on('click', (e) =>{
                    
                    var lat = e.latlng.lat;
                    var lng = e.latlng.lng;

                    markersLayer.clearLayers();
                    L.marker([lat, lng]).addTo(markersLayer);

                    var country_ISO2 = feature.properties.iso;
                    
                    fetch('/trigger-country-update', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ iso: country_ISO2 })
                    })
                    .then(response => response.json())
                    .then(data => {
                        update_country_info(data)
                    })
                })
                
            }
        }).addTo(map);
});

function update_country_info(info){
    document.getElementById("top_line").innerHTML = info.name;
    document.getElementById("top_line2").innerHTML = `native name(s): ${info.native_name}`;
    var table = document.getElementById('info_table_body');

    if(table.rows.length == 0)
        table.insertRow();

    table.rows[0].innerHTML = "";
    table.rows[0].insertCell(0).innerHTML = `<img id="" src="${info.flag_url}" alt="" width=40px></img>`;
    table.rows[0].insertCell(1).innerHTML = info.tld
    table.rows[0].insertCell(2).innerHTML = "+" + info.calling_code
    table.rows[0].insertCell(3).innerHTML = info.driving
    table.rows[0].insertCell(4).innerHTML = info.currency

    document.getElementById("image_grid").innerHTML = `<img id="" src="${info.plate_path}" alt="" width=200px></img>`
    document.getElementById("detail").innerHTML = info.detail
}