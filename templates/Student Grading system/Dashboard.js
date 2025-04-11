document.addEventListener("DOMContentLoaded", function () {
    var sidebarToggle = document.getElementById("sidebarToggle");
    var sidebar = document.getElementById("sidebar");

    sidebarToggle.addEventListener("click", function () {
        // Toggle sidebar active state
        sidebar.classList.toggle("active");
    });
});
