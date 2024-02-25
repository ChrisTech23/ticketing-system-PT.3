import React from 'react';

function TicketDisplay({ tickets }) {
    return (
        <div>
            {/* Heading for the ticket display */}
            <h2>Tickets</h2>
            {/* List to display tickets */}
            <ul>
                {/* Map over the array of tickets and render details for each ticket */}
                {tickets.map(ticket => (
                    <li key={ticket.ticket_id}>
                        {/* Ticket title */}
                        <h3>{ticket.title}</h3>
                        {/* Ticket description */}
                        <p>{ticket.description}</p>
                        {/* Ticket status */}
                        <p>Status: {ticket.status}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TicketDisplay;
