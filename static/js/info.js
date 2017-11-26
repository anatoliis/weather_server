window.onload = function () {
    const valueNames = [
        'avg_temperature',
        'temperature_collector',
        'pressure_mm',
        'humidity',
        'timestamp'
    ];
    const spans = {};
    const ring = document.getElementById('ring');
    const currentTime = document.getElementById('current-time');
    const requestFrequency = 3000;

    valueNames.forEach(function (name) {
        spans[name] = document.getElementById(name);
    });

    function updateInfo(newValues) {
        Object.keys(newValues).forEach(function (key) {
            spans[key].innerText = newValues[key];
        });
        currentTime.innerText = new Date().toTimeString().split(' ')[0];
    }

    function makeRequestAfterTimeout(timeout) {
        setTimeout(makeRequest, timeout || requestFrequency);
    }

    function makeRequest() {
        const r = new XMLHttpRequest();
        r.open('GET', '/update', true);
        r.onload = function () {
            handleResult(true, JSON.parse(r.responseText));
        };
        r.onerror = function () {
            handleResult(false);
        };
        r.send(null);
    }

    function handleResult(success, responseJSON) {
        if (success) {
            updateInfo(responseJSON);
            pulsateRing("green");
        } else {
            pulsateRing("red");
        }
        makeRequestAfterTimeout();
    }

    function pulsateRing(color) {
        ring.style.borderColor = color;
        ring.className = "inforing";
        setTimeout(function () {
            ring.className = "inforing animated";
        }, 100);
    }

    makeRequestAfterTimeout();
};
