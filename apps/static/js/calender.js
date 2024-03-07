document.addEventListener('DOMContentLoaded', function() {
    var events = [
      {
        title: 'Meeting',
        start: '2024-02-28T10:00:00' 
      },
      {
        title: 'Appointment',
        start: '2024-02-28T14:00:00'
      }
    ];

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: events, // Add the events array directly as a property of the options object
      dateClick: function(info) { // Event handler for date click
        alert('Date: ' + info.dateStr); // Show the date string in an alert
        if (info.resource) { // Check if a resource (e.g., event) is associated with the clicked date
          alert('Resource ID: ' + info.resource.id); // Show the resource ID in an alert
        }
      }
    });
    calendar.render(); // Render the calendar after defining the options and events
  });