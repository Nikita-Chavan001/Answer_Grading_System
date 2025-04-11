document.addEventListener("DOMContentLoaded", function () {
    var sidebarToggle = document.getElementById("sidebarToggle");
    var sidebar = document.getElementById("sidebar");
    var mainContent = document.getElementById("main-content");

    sidebarToggle.addEventListener("click", function () {
        sidebar.classList.toggle("active");
        mainContent.style.marginLeft = sidebar.classList.contains("active") ? "440px" : "220px";
    });
});
