// frontend_api_integration.js
// This script fetches live prediction data from your FastAPI backend and updates the UI

async function fetchPrediction() {
  const response = await fetch("https://your-api-url.com/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      price: 0.00042,
      volume: 1000000,
      sentiment: 0.72,
      score: 83
    })
  });

  const data = await response.json();
  updatePredictionCard(data);
}

function updatePredictionCard(data) {
  const output = document.getElementById("prediction-output");
  output.innerHTML = `
    <strong>Prediction:</strong> ${data.prediction}<br>
    <strong>Confidence:</strong> ${data.confidence}%
  `;
}

// Call every 60 seconds
setInterval(fetchPrediction, 60000);
// Run once on load
fetchPrediction();
