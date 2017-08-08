'use strict';

window.onload = function() {
    const valueNames = [
        'avg_temperature',
        'temperature_collector',
        'temperature_unit',
        'pressure_mm',
        'humidity',
        'timestamp'
    ];
    const spans = {};
    valueNames.forEach(name => spans[name] = document.getElementById(name));

    const updateInfo = (spans, newValues) => {
        Object.keys(newValues).forEach(key => {
            spans[key].innerText = newValues[key];
        });
    };

    setInterval(() => {
        const r = new XMLHttpRequest();
        r.open('GET', '/update', true);
        r.onload = function() {
            updateInfo(spans, JSON.parse(r.responseText));
        };
        r.send(null);
    }, 3000)
};
