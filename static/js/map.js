var map = L.map('map').setView([38.0, -20.0], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

fetch('/get-geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: function (feature) {
                return {
                    color: "#0b2e5b",
                    weight: 1,
                    fillOpacity: 0.3
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.name);

                layer.on('click', () =>{
                    var country_ISO2 = feature.properties.ISO_A2;
                    
                    fetch('/trigger-coutry-update', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ ISO2: country_ISO2 })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.url)
                        update_country_info(data)
                    })
                })
                
            }
        }).addTo(map);
});

function update_country_info(info){
    document.getElementById("flag_img").src = info.flag_url;
    document.getElementById("top_line").innerHTML = info.name + " / " + info.native_name;
}