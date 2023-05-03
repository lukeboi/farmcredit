// TO MAKE THE MAP APPEAR YOU MUST
	// ADD YOUR ACCESS TOKEN FROM
	// https://account.mapbox.com
	mapboxgl.accessToken = 'pk.eyJ1IjoibHVrZWZhcnJpdG9yIiwiYSI6ImNsOHVrMWhtdDA0cDIzcG84eXRkMHpnNTgifQ.JYjr4O-AEXVsSDhAYOnEnQ';
    // Create a new map.
    const map = new mapboxgl.Map({
        container: 'map',
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [-96.7, 40.7],
        zoom: 9
    });

    map.on('load', () => {
        // Add a source for the state polygons.
        // map.addSource('states', {
        //     'type': 'geojson',
        //     'data': 'https://docs.mapbox.com/mapbox-gl-js/assets/ne_110m_admin_1_states_provinces_shp.geojson'
        // });

        map.addSource('states', {
            'type': 'geojson',
            'data': '/static/geo.geojson'
        });

        // Add a layer showing the state polygons.
        map.addLayer({
            'id': 'states-layer',
            'type': 'fill',
            'source': 'states',
            'paint': {
                'fill-color': 'rgba(200, 100, 240, 0.4)',
                'fill-outline-color': 'rgba(200, 100, 240, 1)'
            }
        });

        // When a click event occurs on a feature in the states layer,
        // open a popup at the location of the click, with description
        // HTML from the click event's properties.
        map.on('click', 'states-layer', (e) => {
            var apn = Math.floor(Math.random() * 10 ** 10);
            new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(e.features[0].properties.name + "<br> APN: " + apn)
                .addTo(map);
            fetch("/api/" + e.features[0].properties.name)
            .then(response=>response.text())
            .then(data=>{ 
                console.log(data);
                document.getElementById("info-desc").innerHTML = "<b>APN:</b> " + apn + "<br>" + data;
            });
            document.getElementById("info-title").innerHTML = "<b>Selected field name:</b> " + e.features[0].properties.name;
        });

        // Change the cursor to a pointer when
        // the mouse is over the states layer.
        map.on('mouseenter', 'states-layer', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        // Change the cursor back to a pointer
        // when it leaves the states layer.
        map.on('mouseleave', 'states-layer', () => {
            map.getCanvas().style.cursor = '';
        });
    });