document.addEventListener("DOMContentLoaded", function() {
    // Handle the form submission
    document.getElementById('uploadForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(this); // Using 'this' to get the form data

        // Show message before the request is made
        const messageDiv = document.getElementById('message');
        messageDiv.innerHTML = `<div class="alert alert-info">Uploading...</div>`;

        try {
            // Send the form data to the backend
            const response = await fetch('/dashboard', {
                method: 'POST',
                body: formData
            });

            // Handle the response
            const result = await response.json();
            if (response.ok) {
                // Success: Show the success message
                messageDiv.innerHTML = `<div class="alert alert-success">${result.message}</div>`;
                // Optionally, clear the form or update UI
                document.getElementById('uploadForm').reset();
            } else {
                // Failure: Show the error message
                messageDiv.innerHTML = `<div class="alert alert-danger">${result.message}</div>`;
            }
        } catch (error) {
            // In case of network or unexpected errors
            messageDiv.innerHTML = `<div class="alert alert-danger">An error occurred while uploading the file.</div>`;
        }
    });
});
document.getElementById("sidebarToggle").addEventListener("click", function() {
    var sidebar = document.getElementById("sidebar");
    var mainContent = document.querySelector("main");

    // Toggle sidebar active class
    sidebar.classList.toggle("active");

    // Toggle main content margin when sidebar is active
    if (sidebar.classList.contains("active")) {
        mainContent.style.marginLeft = "220px";  // Adjust to match the sidebar width
    } else {
        mainContent.style.marginLeft = "0";      // Reset when sidebar is hidden
    }
});

// Handling file uploads
document.getElementById("uploadBtn").addEventListener("click", function() {
    var fileInput = document.getElementById("fileInput");
    var fileDisplayArea = document.getElementById("fileDisplayArea");

    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var fileLink = document.createElement("a");
        fileLink.href = URL.createObjectURL(file);
        fileLink.target = "_blank";
        fileLink.textContent = file.name;
        
        fileDisplayArea.innerHTML = "File uploaded: ";
        fileDisplayArea.appendChild(fileLink);
        fileDisplayArea.style.display = "block";
    } else {
        alert("Please select a file first.");
    }
});

// Handling file uploads for the second card
document.getElementById("uploadBtn2").addEventListener("click", function() {
    var fileInput = document.getElementById("fileInput2");
    var fileDisplayArea = document.getElementById("fileDisplayArea2");

    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var fileLink = document.createElement("a");
        fileLink.href = URL.createObjectURL(file);
        fileLink.target = "_blank";
        fileLink.textContent = file.name;
        
        fileDisplayArea.innerHTML = "File uploaded: ";
        fileDisplayArea.appendChild(fileLink);
        fileDisplayArea.style.display = "block";
    } else {
        alert("Please select a file first.");
    }
});
