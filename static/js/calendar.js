



document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');

    fetch('/api/cycle-calendar/')  // Fetch events from Django API
        .then(response => response.json())
        .then(events => {
            let calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                selectable: true,
                editable: false,
                events: events,  // Load cycle data from backend
            });
            calendar.render();
        })
        .catch(error => console.error("Error fetching cycle data:", error));
});
