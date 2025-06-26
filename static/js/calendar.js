
document.addEventListener('DOMContentLoaded', function () {

    const cycleButton = document.getElementById("#cycleButton");

    cycleButton.addEventListener('onclick', (event) => {
        event.preventDefault();

        const cycleResults = document.getElementById("cycleResults");
        cycleResults.classList.remove("hidden");
    })





});



