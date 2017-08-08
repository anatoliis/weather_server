'use strict';

const CHART_COLORS = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)',
    black: 'rgb(0, 0, 0)',
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
    const day = date.getDate();
    const month = date.getMonth();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    return pad(day) + '.' + pad(month) + ' | ' + pad(hours) + ':' + pad(minutes);
};

const getLabels = (datasets) => {
    return datasets.timestamp.map(ts => formatDate(new Date(ts * 1000)));
};

const getDatasetByName = (datasets, name) => {
    return datasets[name];
};

const getConfig = (labels, avg_temperature, temperature_collector, humidity, pressure) => {
    return {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Наружная',
                    backgroundColor: CHART_COLORS.green,
                    borderColor: CHART_COLORS.green,
                    fill: false,
                    data: avg_temperature,
                    cubicInterpolationMode: 'monotone',
                    yAxisID: 'temperature'
                },
                {
                    label: 'Коллектор',
                    backgroundColor: CHART_COLORS.red,
                    borderColor: CHART_COLORS.red,
                    fill: false,
                    data: temperature_collector,
                    cubicInterpolationMode: 'monotone',
                    yAxisID: 'temperature'
                },
                {
                    label: 'Влажность',
                    backgroundColor: CHART_COLORS.blue,
                    borderColor: CHART_COLORS.blue,
                    fill: false,
                    data: humidity,
                    cubicInterpolationMode: 'monotone',
                    yAxisID: 'humidity'
                },
                {
                    label: 'Давление',
                    backgroundColor: CHART_COLORS.black,
                    borderColor: CHART_COLORS.black,
                    fill: false,
                    data: pressure,
                    cubicInterpolationMode: 'monotone',
                    yAxisID: 'pressure'
                },
            ],
        },
        options: {
            responsive: true,
            title:{
                display:false,
                text:'График'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            elements: {
                point: {
                    radius: 0,
                    hitRadius: 3,
                    hoverRadius: 3,
                }
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Время'
                    }
                }],
                yAxes: [
                    {
                        id: 'temperature',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Температура'
                        },
                        ticks: {
                            min: 0,
                            suggestedMin: 0,
                            max: 105,
                            autoSkip: true
                        }
                    },
                    {
                        id: 'humidity',
                        display: true,
                        position: 'right',
                        scaleLabel: {
                            display: true,
                            labelString: 'Влажность'
                        },
                        ticks: {
                            min: 0,
                            max: 100,
                            autoSkip: true
                        }
                    },
                    {
                        id: 'pressure',
                        display: true,
                        position: 'right',
                        scaleLabel: {
                            display: true,
                            labelString: 'Давление'
                        },
                        ticks: {
                            min: 745,
                            max: 760,
                            autoSkip: true
                        }
                    }
                ]
            }
        }
    }
};

window.onload = function() {
    const ctx = document.getElementById("canvas").getContext("2d");

    let rawData = getMeasurementsData();
    const datasets = convertToDatasets(rawData);
    const labels = getLabels(datasets);
    const avg_temperature = getDatasetByName(datasets, 'temperature_1');
    const collector_temp = getDatasetByName(datasets, 'temperature_collector');
    const humidity = getDatasetByName(datasets, 'humidity');
    const pressure = getDatasetByName(datasets, 'pressure_mm');
    const config = getConfig(labels, avg_temperature, collector_temp, humidity, pressure);

    window.myLine = new Chart(ctx, config);
};
