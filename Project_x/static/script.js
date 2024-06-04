function sendVideoId() {
    var videoId = document.getElementById('videoIdInput').value;

    if (videoId.trim() === "") {
        console.error('Please enter a valid YouTube Video ID');
        return;
    }

    // Send the video ID to the Flask backend
    $.ajax({
        type: 'POST',
        url: '/process_video_id',
        data: { video_id: videoId },
        success: function(response) {
            console.log(response);
            // Handle success response from Flask
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
            // Handle error response from Flask
        }
    });
}
