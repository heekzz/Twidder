var countryData = new Map();
var genderData = new Map();
var onlineTimestamps = [];
var onlineUsers = [];
var onlineChart;
var genderChart;
var countryChart;

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
    var date = new Date().toLocaleTimeString("sv-SE");
    var oc = document.getElementById("onlineChart");
    onlineUsers = [0, 0, 0, 0, 0, 0];
    onlineTimestamps = [date,date,date,date,date,date,]
    onlineChart = new Chart(oc, {
        type: 'line',
        data: {
            labels: [date, date, date, date, date, date],
            datasets: [{
                label: 'Online users',
                data: onlineUsers,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: 10
                    }
                }],
                xAxes : [ {
                    gridLines : {
                        display : false
                    }
                } ]
            }
        }
    });

}

// Updates the data in the chart
function updateChartData(data) {
    genderData.clear();
    var users = data["users"];
    console.log(users)
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

    // Assign data
    onlineUsers.push(data["online"]);
    onlineUsers.shift();

    genderChart.data.labels =  Array.from(genderData.keys());
    genderChart.data.datasets[0].data = Array.from(genderData.values());

    countryChart.data.labels =  Array.from(countryData.keys());
    countryChart.data.datasets[0].data = Array.from(countryData.values());

    // Update charts
    genderChart.update();
    countryChart.update();
}

function updateCharts(data) {
    updateChartData(data)

}

setInterval(function(){
    onlineTimestamps.push(new Date().toLocaleTimeString("sv-SE"));
    onlineTimestamps.shift();

    onlineUsers.push(onlineUsers[onlineUsers.length - 1]);
    onlineUsers.shift();
    console.log(onlineUsers)
    onlineChart.data.datasets[0].data = onlineUsers;
    onlineChart.data.labels = onlineTimestamps;
    onlineChart.update();
}, 5000);