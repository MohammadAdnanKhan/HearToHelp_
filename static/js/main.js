function analyzeAudio() {
    const audioFile = document.getElementById('audioFile').files[0];
    const confidenceBar = document.getElementById('confidenceBar');
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
                const probabilities = data.probabilities; // this is a dictionary with all the probabilities and their values

                // Display the result
                document.getElementById('resultsDiv').innerHTML = `
                <h3 class="text-center">Analysis Result</h3>
                <p class="text-center">Emotion: ${emotion}</p>
                <p class="text-center">Confidence: ${confidence}%</p>

                <div id="confPerc">
                    <div id="confidenceBar" style="width: ${parseInt(confidence)}%;">
                        ${parseInt(confidence)}%
                    </div>
                </div>
            `;
                // Save the result to local storage
                const pastResults = localStorage.getItem('pastResults');
                if (pastResults) {
                    const resultsObj = JSON.parse(pastResults);
                    resultsObj.push({
                        date: new Date().toLocaleString(),
                        emotion: emotion,
                        confidence: data.confidence
                    });
                    localStorage.setItem('pastResults', JSON.stringify(resultsObj));
                } else {
                    localStorage.setItem('pastResults', JSON.stringify([{
                        date: new Date().toLocaleString(),
                        emotion: emotion,
                        confidence: data.confidence
                    }]));
                }

                // Update the past results table
                showPastResults();
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

const showPastResults = () => {
    const resultsTableBody = document.getElementById('resultsTableBody');
    const pastResults = localStorage.getItem('pastResults');

    if (pastResults) {
        resultsTableBody.innerHTML = ''; // Clear the table body
        const resultsObj = JSON.parse(pastResults);
        // <tr>
        //     <td>2023-10-01 12:00</td>
        //     <td>Positive</td>
        //     <td>95%</td>
        // </tr>
        resultsObj.forEach(result => {
            const row = document.createElement('tr');
            row.innerHTML = `
            <td>${result.date}</td>
            <td>${result.emotion}</td>
            <td>${(result.confidence * 100).toFixed(2)}%</td>
        `;
            resultsTableBody.appendChild(row);
        });
    } else {
        resultsTableBody.innerHTML = `
        <tr>
            <td colspan="3" class="text-center">No past results found</td>
        </tr>
    `;
    }
}

window.onload = function () {
    showPastResults();
}