function analyzeAudio() {
    const audioFile = document.getElementById('audioFile').files[0];

    // Check if the user has uploaded a file
    if (!audioFile) {
        alert('Please upload an audio file');
        return;
    }

    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append("audio", audioFile);

    // Show loading indicator
    document.getElementById('resultsDiv').innerHTML = `
        <h3 class="text-center">Processing...</h3>
        <p class="text-center">Please wait while we analyze the audio.</p>
    `;

    // Send the audio file to the server via FormData
    fetch('/api/detect', {
        method: 'POST',
        body: formData // Send the FormData with the audio file
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('resultsDiv').innerHTML = `
                <h3 class="text-center">Error</h3>
                <p class="text-center">${data.error}</p>
            `;
            } else {
                const emotion = data.emotion;
                const confidence = (data.confidence * 100).toFixed(2); // Convert confidence to percentage

                // Display the result
                document.getElementById('resultsDiv').innerHTML = `
                <h3 class="text-center">Analysis Result</h3>
                <p class="text-center">Emotion: ${emotion}</p>
                <p class="text-center">Confidence: ${confidence}%</p>
            `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultsDiv').innerHTML = `
            <h3 class="text-center">Error</h3>
            <p class="text-center">Something went wrong. Please try again later.</p>
        `;
        });
}
