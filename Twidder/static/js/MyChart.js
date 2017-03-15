var countryData = new Map();
var genderData = new Map();
var onlineTimestamps = [0];
var onlineUsers = [0];
var onlineChart;
var genderChart;
var countryChart;
var isPaused = false;

// Creates charts
function loadChart() {
    Chart.defaults.global.showScale = "false";
    var gc = document.getElementById("genderChart");
    genderChart = new Chart(gc, {
        type: 'pie',
        data: {
            labels: Array.from(genderData.keys()),
            datasets: [{
                label: 'Gender',
                data: Array.from(genderData.values()),
                backgroundColor: [
                    "#ea1e00",
                    "#020201",
                    "#8d4f23"
                ],
                hoverBackgroundColor: [
                    "#b54b43",
                    "#424242",
                    "#664011"
                ],
                borderWidth: 1
            }]
        },
        options: {

        }
    });
    var cc = document.getElementById("countryChart");
    countryChart = new Chart(cc, {
        type: 'pie',
        data: {
            labels: Array.from(countryData.keys()),
            datasets: [{
                label: 'Gender',
                data: Array.from(countryData.values()),
                backgroundColor: [
                    "#ea1e00",
                    "#020201",
                    "#8d4f23",
                    "#ff800a",
                    "#e687b0",
                    "#67ca0c",
                    "#4649f7",
                    "#0b8b8d",
                    "#87188d",
                    "#b2b6b8"
                ],
                hoverBackgroundColor: [
                    "#b54b43",
                    "#424242",
                    "#664011",
                    "#735c03",
                    "#8f007a",
                    "#3e7b0b",
                    "#21237a",
                    "#09494b",
                    "#480037",
                    "#535759"
                ],
                borderWidth: 1
            }]
        },
        options: {

        }
    });
    var oc = document.getElementById("onlineChart");
    // onlineTimestamps = [date];
    // onlineUsers = [0];
    onlineChart = new Chart(oc, {
        type: 'line',
        data: {
            labels: onlineTimestamps,
            datasets: [{
                label: 'Online users',
                data: onlineUsers,
                borderColor: "#ea1e00",
                backgroundColor: "#b54b43",
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 5,
                        fixedStepSize: 1
                    }
                }],
                xAxes : [ {
                    gridLines : {
                        display : false
                    }
                } ],
            }
        }
    });

}

// Updates the data in the chart
function updateChartData(data) {
    isPaused = true;
    genderData.clear();
    countryData.clear();
    var users = data["users"];

    for (var i = 0; i < users.length; i++) {
        var user = users[i];
        // Gender
        if (genderData.has(user.gender)) {
            var tot = genderData.get(user.gender);
            genderData.delete(user.gender);
            tot += 1;
            genderData.set(user.gender, tot);
        } else {
            genderData.set(user.gender, 1);
        }

        // Reformat country to start with uppercase letter
        var formatCountry = user.country.toLowerCase();
        formatCountry = formatCountry[0].toUpperCase() + formatCountry.substr(1);

        // Country
        if (countryData.has(formatCountry)) {
            var tot = countryData.get(formatCountry);
            countryData.delete(formatCountry);
            tot += 1;
            countryData.set(formatCountry, tot);
        } else {
            countryData.set(formatCountry, 1);
        }

    }

    // Online users
    onlineUsers.push(data["online"]);
    if(onlineUsers.length > 6)
        onlineUsers.shift();
    onlineTimestamps.push(new Date().toLocaleTimeString("sv-SE"));
    if(onlineTimestamps.length > 6)
        onlineTimestamps.shift();

    if (typeof genderChart !== "undefined" && typeof countryChart !== "undefined" && typeof onlineChart !== "undefined") {
        // Assign data
        genderChart.data.labels =  Array.from(genderData.keys());
        genderChart.data.datasets[0].data = Array.from(genderData.values());

        countryChart.data.labels =  Array.from(countryData.keys());
        countryChart.data.datasets[0].data = Array.from(countryData.values());

        // Update charts
        genderChart.update();
        countryChart.update();
        onlineChart.update();
    }
    isPaused = false;
}

function updateCharts(data) {
    updateChartData(data)

}

