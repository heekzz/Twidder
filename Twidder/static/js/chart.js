var countryData = new Map();
var genderData = new Map();

function loadChart() {

    var gc = document.getElementById("genderChart");
    var genderChart = new Chart(gc, {
        type: 'pie',
        data: {
            labels: Array.from(genderData.keys()),
            datasets: [{
                label: 'Gender',
                data: Array.from(genderData.values()),
                backgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56"
                ],
                hoverBackgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56"
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

}

function updateChartData(data) {
    genderData.clear();

    for (var i = 0; i < data.length; i++) {
        var user = data[i];
        // Gender
        if (genderData.has(user.gender)) {
            var tot = genderData.get(user.gender);
            genderData.delete(user.gender);
            tot += 1;
            genderData.set(user.gender, tot);
        } else {
            genderData.set(user.gender, 1);
        }

        if (countryData.has(user.country)) {

        }

    }

    console.log(Array.from(genderData.keys()));
}

function updateCharts(data) {
    updateChartData(data)

}