import React from 'react';
import { Link } from 'react-router-dom';
import './EventCard.css';

const EventCard = ({ event }) => {
  return (
    <div className="event-card">
      <div className="event-header">
        <h3 className="event-title">{event.name}</h3>
        <span className="event-location">{event.location}</span>
      </div>

      <div className="event-details">
        <p className="event-description">{event.description}</p>
        <div className="event-dates">
          <span>Start: {new Date(event.start_date).toLocaleDateString()}</span>
          <span>End: {new Date(event.end_date).toLocaleDateString()}</span>
        </div>
      </div>

      <div className="event-actions">
        <Link to={`/events/${event.event_id}/booths`} className="view-booths-btn">
          View Booths
        </Link>
      </div>
    </div>
  );
};

export default EventCard;