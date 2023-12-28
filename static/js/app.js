const ctx = document.getElementById('live-chart');
const apiUrl = 'http://localhost:8008/live_data/Test_Sensor/';

var lable_list = [];
var data_list = [];
let data_dict = [];

async function fetchData() {
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Fetch operation failed:', error);
    }
}

// Function to create a chart with the fetched data
async function createChart() {
    const apiData = await fetchData();

    // Extract labels and data from the API response
    const labels = apiData.map(item => item.read_time);
    const data = apiData.map(item => item.read_value);

    // Create a bar chart using Chart.js
    const ctx = document.getElementById('live-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
        labels: labels,
        datasets: [{
            label: 'Sensor Value',
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 8
        }]
        },
        options: {
        scales: {
            y: {
            // beginAtZero: true
            suggestedMin: 0,
            suggestedMax: 100
            }
        },
        animation: {
            // Disable all animations
            duration: 0
        }
        }
    });
    return myChart;
}
// Function to refresh the chart
async function refreshChart(myChart) {
    const apiData = await fetchData();

    // Extract labels and data from the updated API response
    const labels = apiData.map(item => item.read_time);
    const data = apiData.map(item => item.read_value);

    // Update the chart data
    //const myChart = Chart.getChart('myChart');
    myChart.data.labels = labels;
    myChart.data.datasets[0].data = data;
    myChart.update();
  }
// Initial creation of the chart
const myChartPromise = createChart();

// Auto-refresh the chart every 5 seconds (adjust as needed)
setInterval(async () => {
    const myChart = await myChartPromise;
    refreshChart(myChart);
}, 2000);
