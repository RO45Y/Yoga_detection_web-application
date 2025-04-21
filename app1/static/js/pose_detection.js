
let videoElement = document.getElementById("webcam");
let tryPoseButton = document.getElementById("tryPoseButton");
let statusDiv = document.getElementById("status");
let resultDiv = document.getElementById("result");

// Set up webcam stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        videoElement.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing webcam: ", err);
        statusDiv.textContent = "Error accessing webcam.";
    });

// Capture an image from the webcam
function captureImage() {
    let canvas = document.createElement("canvas");
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    let ctx = canvas.getContext("2d");
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL("image/jpeg");
}

// Send image to backend
async function sendPoseData(poseName, imageData) {
    try {
        statusDiv.textContent = "Processing pose...";
        let response = await fetch(`/pose_detection/${poseName}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });

        let data = await response.json();

        if (response.ok) {
            // Process response data
            if (data.poseStatus === 'correct') {
                resultDiv.innerHTML = `<p>Pose Correct!</p><img src="data:image/jpeg;base64,${data.landmarkImage}" alt="Pose with landmarks"/>`;
            } else if (data.poseStatus === 'incorrect') {
                resultDiv.innerHTML = `<p>Pose Incorrect. Please try again.</p>`;
            } else {
                resultDiv.innerHTML = `<p>No landmarks detected.</p>`;
            }
        } else {
            resultDiv.innerHTML = `<p>Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

// Button click event
tryPoseButton.addEventListener("click", () => {
    let imageData = captureImage();
    sendPoseData("{{ pose_name }}", imageData); // Replace with the actual pose name dynamically
});
