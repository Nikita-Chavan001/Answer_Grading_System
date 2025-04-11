document.getElementById("sidebarToggle").addEventListener("click", function() {
    var sidebar = document.getElementById("sidebar");
    var mainContent = document.querySelector("main");

    // Toggle sidebar active class
    sidebar.classList.toggle("active");

    // Toggle main content margin when sidebar is active
    if (sidebar.classList.contains("active")) {
        mainContent.style.marginLeft = "220px"; // Adjust to match the sidebar width
    } else {
        mainContent.style.marginLeft = "0"; // Reset when sidebar is hidden
    }
});

// Handling view assignments button for the first card
document.getElementById("viewAssignmentsBtn").addEventListener("click", function() {
    alert("Viewing uploaded assignments for WAP to implement Find-S Algorithm.");
});

// Handling view assignments button for the second card
document.getElementById("viewAssignmentsBtn2").addEventListener("click", function() {
    alert("Viewing uploaded assignments for WAP to implement Find-S Algorithm.");
});

// Handling view assignments button for the third card
document.getElementById("viewAssignmentsBtn3").addEventListener("click", function() {
    alert("Viewing uploaded assignments for WAP to implement Find-S Algorithm.");
});
