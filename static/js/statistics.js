document.addEventListener('DOMContentLoaded', async () => {
  const ctx = document.getElementById('barChart').getContext('2d');

  // Fetch the data from the API
  const response = await fetch('/chart-data');
  const data = await response.json();

  // Create the chart with fetched data
  new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [
              {
                  label: 'Applications',
                  data: data.applications, // Use dynamic data here
                  backgroundColor: 'rgba(128, 0, 128, 0.6)',
              },
              {
                  label: 'Shortlisted',
                  data: data.shortlisted, // Use dynamic data here
                  backgroundColor: 'rgba(0, 128, 0, 0.6)',
              },
          ],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
      },
  });
});
const ctxStatistics = document.getElementById('statisticsChart').getContext('2d');
new Chart(ctxStatistics, {
  type: 'bar',
  data: {
    labels: ['$98', '$108', '$83', '$123', '$41'], // X-axis labels
    datasets: [
      {
        label: 'Statistics',
        data: [98, 108, 83, 123, 41], // Data points
        backgroundColor: [
          '#d3d3d3', '#d3d3d3', '#d3d3d3', '#4caf50', '#d3d3d3'
        ],
        borderWidth: 0,
        borderRadius: 5, // Rounded corners for bars
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false, // Hide legend
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        grid: {
          drawBorder: false,
          color: '#f0f0f0',
        },
        ticks: {
          beginAtZero: true,
        },
      },
    },
  },
});