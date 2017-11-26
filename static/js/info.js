window.onload = function () {
    const valueNames = [
        'avg_temperature',
        'temperature_collector',
        'pressure_mm',
        'humidity',
        'timestamp'
    ];
    const spans = {};
    const receiveTimeRing = document.getElementById('receive-ring');
    const currentTimeRing = document.getElementById('current-ring');
    const currentTime = document.getElementById('current-time');
    const requestFrequency = 3000;

    valueNames.forEach(function (name) {
        spans[name] = document.getElementById(name);
    });

    function updateInfo(newValues) {
        Object.keys(newValues).forEach(function (key) {
            updateField(key, spans[key], newValues[key]);
        });
        updateCurrentTime();
    }

    function updateField(key, span, value) {

        if (span.innerText !== value) {
            if (key === 'timestamp') {
                pulsateRing(receiveTimeRing, 'green');
            }
            span.innerText = value;
        }
    }

    function updateCurrentTime() {
        currentTime.className = "current-time";
        setTimeout(function () {
            currentTime.className = "current-time animated";
        }, 10);
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
            pulsateRing(currentTimeRing, "green");
        } else {
            pulsateRing(currentTimeRing, "red");
        }
        makeRequestAfterTimeout();
    }

    function pulsateRing(ring, color) {
        ring.style.borderColor = color;
        ring.className = "inforing";
        setTimeout(function () {
            ring.className = "inforing animated";
        }, 10);
    }

    makeRequestAfterTimeout();
};
