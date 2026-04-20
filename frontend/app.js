const video = document.getElementById('videoPlayer');
const canvas = document.getElementById('glassCanvas');
const ctx = canvas.getContext('2d');
const statusText = document.getElementById('status');
const personCountUI = document.getElementById('personCount');
const vehicleCountUI = document.getElementById('vehicleCount');

video.addEventListener('loadedmetadata', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
});

const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    statusText.innerText = "SYS_STATUS: PIPELINE SECURE";
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const predictions = data.detections;
    const insights = data.insights;
    
    // Update the UI Insights
    personCountUI.innerText = insights.person;
    vehicleCountUI.innerText = insights.vehicle;

    // Wipe the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Paint boxes exactly like the OLY Store Sync image
    predictions.forEach(box => {
        const x = box.x1;
        const y = box.y1;
        const width = box.x2 - box.x1;
        const height = box.y2 - box.y1;

        // Draw the box (Changed to red to match their UI)
        ctx.strokeStyle = '#ff0033';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, width, height);

        // Draw background for the text label
        const labelText = `${box.label.toUpperCase()} ${box.track_id}`;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        const textWidth = ctx.measureText(labelText).width;
        ctx.fillRect(x, y - 25, textWidth + 15, 25);

        // Draw the text (Shows "PERSON 13" just like their site)
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 16px Arial';
        ctx.fillText(labelText, x + 5, y - 7);
    });
};

ws.onclose = () => {
    statusText.innerText = "SYS_STATUS: CRITICAL FAILURE";
    statusText.style.color = "#ff3333";
};