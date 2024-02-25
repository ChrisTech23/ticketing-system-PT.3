import React from 'react';
import { useParams } from 'react-router-dom';
import GetTicket from './components/GetTicket';

function TicketDetailsPage() {
    // Get ticket ID from URL parameters
    const { id } = useParams();

    return (
        <div>
            {/* Render GetTicket component and pass ticketId as prop */}
            <GetTicket ticketId={id} />
        </div>
    );
}

export default TicketDetailsPage;
