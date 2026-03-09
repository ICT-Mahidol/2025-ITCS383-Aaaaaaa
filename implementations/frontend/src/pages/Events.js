import React, { useState, useEffect } from 'react';
import { eventService } from '../services/api';
import EventCard from '../components/EventCard';
import './Events.css';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await eventService.getEvents();
      setEvents(response.data);
    } catch (err) {
      setError('Failed to load events');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading events...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="events-page">
      <div className="page-header">
        <h1>Events</h1>
        <p>Discover and book booths for upcoming events</p>
      </div>

      <div className="events-grid">
        {events.length === 0 ? (
          <div className="no-events">
            <h3>No events available</h3>
            <p>Check back later for upcoming events</p>
          </div>
        ) : (
          events.map(event => (
            <EventCard key={event.event_id} event={event} />
          ))
        )}
      </div>
    </div>
  );
};

export default Events;