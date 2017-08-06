'use strict';

const CHART_COLORS = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

const getMeasurementsData = () => {
    return JSON.parse(document.getElementById('json_data').innerText);
};

const convertToDatasets = (rawData) => {
    const datasets = {};
    const keys = Object.keys(rawData[0] || {});

    rawData.forEach(measurement => {
        keys.forEach(key => {
            if (datasets[key] !== undefined) {
                datasets[key].push(measurement[key]);
            }
            else {
                datasets[key] = [measurement[key]];
            }
        })
    });
    return datasets;
};

const pad = (number) => {
    return ('0' + number).substr(-2);
};

const formatDate = (date) => {
    const hours = date.getHours();
    const minutes = date.getMinutes();
    return pad(hours) + ':' + pad(minutes);
};

const getLabels = (datasets) => {
    return datasets.timestamp.map(ts => formatDate(new Date(ts * 1000)));
};

const getDatasetByName = (datasets, name) => {
    return datasets[name];
};

const getConfig = (labels, temp1) => {
    return {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Температура 1',
                backgroundColor: CHART_COLORS.red,
                borderColor: CHART_COLORS.red,
                fill: false,
                data: temp1
            }],
        },
        options: {
            responsive: true,
            title:{
                display:true,
                text:'График температуры за последние 12 часов'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Время'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Значение'
                    }
                }]
            }
        }
    }
};

window.onload = function() {
    const ctx = document.getElementById("canvas").getContext("2d");

    const rawData = getMeasurementsData();
    const datasets = convertToDatasets(rawData);
    const labels = getLabels(datasets);
    const temp1 = getDatasetByName(datasets, 'temperature_1');
    const config = getConfig(labels, temp1);

    window.myLine = new Chart(ctx, config);
};
