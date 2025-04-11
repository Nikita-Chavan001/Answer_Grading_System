document.addEventListener("DOMContentLoaded", function () {
    var sidebarToggle = document.getElementById("sidebarToggle");
    var sidebar = document.getElementById("sidebar");
    var toggleCards = document.getElementById("toggleCards");
    var courseCards = document.querySelectorAll(".course-card");

    sidebarToggle.addEventListener("click", function () {
        // Toggle sidebar active state
        sidebar.classList.toggle("active");

        // Adjust button's position based on sidebar state
        if (sidebar.classList.contains("active")) {
            sidebarToggle.style.left = "220px";
        } else {
            sidebarToggle.style.left = "0px";
        }
    });

    toggleCards.addEventListener("click", function () {
        // Toggle visibility of course cards
        courseCards.forEach(function (card) {
            card.classList.toggle("hidden");
        });
    });
});
