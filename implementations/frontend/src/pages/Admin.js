import React, { useState, useEffect } from 'react';
import { eventService, boothService } from '../services/api';
import './Admin.css';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('events');
  const [events, setEvents] = useState([]);
  const [booths, setBooths] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showEventForm, setShowEventForm] = useState(false);
  const [showBoothForm, setShowBoothForm] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState('');

  const [eventForm, setEventForm] = useState({
    name: '',
    description: '',
    location: '',
    start_date: '',
    end_date: ''
  });

  const [boothForm, setBoothForm] = useState({
    booth_number: '',
    size: '',
    price: '',
    type: 'INDOOR',
    classification: 'TEMPORARY',
    duration_type: 'SHORT_TERM',
    electricity: false,
    water_supply: false,
    outlets: 0
  });

  useEffect(() => {
    if (activeTab === 'events') {
      fetchEvents();
    }
  }, [activeTab]);

  const fetchEvents = async () => {
    try {
      const response = await eventService.getEvents();
      setEvents(response.data);
    } catch (err) {
      console.error('Failed to fetch events:', err);
    }
  };

  const fetchBooths = async (eventId) => {
    try {
      const response = await boothService.getBoothsByEvent(eventId);
      setBooths(response.data);
    } catch (err) {
      console.error('Failed to fetch booths:', err);
    }
  };

  const handleEventSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await eventService.createEvent(eventForm);
      setEventForm({
        name: '',
        description: '',
        location: '',
        start_date: '',
        end_date: ''
      });
      setShowEventForm(false);
      fetchEvents();
    } catch (err) {
      alert('Failed to create event');
    } finally {
      setLoading(false);
    }
  };

  const handleBoothSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await boothService.createBooth({
        ...boothForm,
        event_id: selectedEvent
      });
      setBoothForm({
        booth_number: '',
        size: '',
        price: '',
        type: 'INDOOR',
        classification: 'TEMPORARY',
        duration_type: 'SHORT_TERM',
        electricity: false,
        water_supply: false,
        outlets: 0
      });
      setShowBoothForm(false);
      if (selectedEvent) {
        fetchBooths(selectedEvent);
      }
    } catch (err) {
      alert('Failed to create booth');
    } finally {
      setLoading(false);
    }
  };

  const handleEventSelect = (eventId) => {
    setSelectedEvent(eventId);
    fetchBooths(eventId);
  };

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
      </div>

      <div className="admin-tabs">
        <button
          className={activeTab === 'events' ? 'active' : ''}
          onClick={() => setActiveTab('events')}
        >
          Manage Events
        </button>
        <button
          className={activeTab === 'booths' ? 'active' : ''}
          onClick={() => setActiveTab('booths')}
        >
          Manage Booths
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'events' && (
          <div className="events-section">
            <div className="section-header">
              <h2>Events</h2>
              <button
                className="add-btn"
                onClick={() => setShowEventForm(!showEventForm)}
              >
                {showEventForm ? 'Cancel' : 'Add Event'}
              </button>
            </div>

            {showEventForm && (
              <form className="admin-form" onSubmit={handleEventSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label>Name</label>
                    <input
                      type="text"
                      value={eventForm.name}
                      onChange={(e) => setEventForm({...eventForm, name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Location</label>
                    <input
                      type="text"
                      value={eventForm.location}
                      onChange={(e) => setEventForm({...eventForm, location: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={eventForm.description}
                    onChange={(e) => setEventForm({...eventForm, description: e.target.value})}
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Start Date</label>
                    <input
                      type="date"
                      value={eventForm.start_date}
                      onChange={(e) => setEventForm({...eventForm, start_date: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>End Date</label>
                    <input
                      type="date"
                      value={eventForm.end_date}
                      onChange={(e) => setEventForm({...eventForm, end_date: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <button type="submit" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Event'}
                </button>
              </form>
            )}

            <div className="events-list">
              {events.map(event => (
                <div key={event.event_id} className="event-item">
                  <div className="event-info">
                    <h3>{event.name}</h3>
                    <p>{event.location}</p>
                    <p>{new Date(event.start_date).toLocaleDateString()} - {new Date(event.end_date).toLocaleDateString()}</p>
                  </div>
                  <button
                    className="manage-booths-btn"
                    onClick={() => {
                      setActiveTab('booths');
                      handleEventSelect(event.event_id);
                    }}
                  >
                    Manage Booths
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'booths' && (
          <div className="booths-section">
            <div className="section-header">
              <h2>Booths</h2>
              <div>
                <select
                  value={selectedEvent}
                  onChange={(e) => handleEventSelect(e.target.value)}
                  className="event-select"
                >
                  <option value="">Select Event</option>
                  {events.map(event => (
                    <option key={event.event_id} value={event.event_id}>
                      {event.name}
                    </option>
                  ))}
                </select>
                {selectedEvent && (
                  <button
                    className="add-btn"
                    onClick={() => setShowBoothForm(!showBoothForm)}
                  >
                    {showBoothForm ? 'Cancel' : 'Add Booth'}
                  </button>
                )}
              </div>
            </div>

            {showBoothForm && selectedEvent && (
              <form className="admin-form" onSubmit={handleBoothSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label>Booth Number</label>
                    <input
                      type="text"
                      value={boothForm.booth_number}
                      onChange={(e) => setBoothForm({...boothForm, booth_number: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Size</label>
                    <input
                      type="text"
                      value={boothForm.size}
                      onChange={(e) => setBoothForm({...boothForm, size: e.target.value})}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Price</label>
                    <input
                      type="number"
                      step="0.01"
                      value={boothForm.price}
                      onChange={(e) => setBoothForm({...boothForm, price: e.target.value})}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Type</label>
                    <select
                      value={boothForm.type}
                      onChange={(e) => setBoothForm({...boothForm, type: e.target.value})}
                    >
                      <option value="INDOOR">Indoor</option>
                      <option value="OUTDOOR">Outdoor</option>
                    </select>
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Classification</label>
                    <select
                      value={boothForm.classification}
                      onChange={(e) => setBoothForm({...boothForm, classification: e.target.value})}
                    >
                      <option value="FIXED">Fixed</option>
                      <option value="TEMPORARY">Temporary</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Duration Type</label>
                    <select
                      value={boothForm.duration_type}
                      onChange={(e) => setBoothForm({...boothForm, duration_type: e.target.value})}
                    >
                      <option value="SHORT_TERM">Short Term</option>
                      <option value="LONG_TERM">Long Term</option>
                    </select>
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Electricity</label>
                    <input
                      type="checkbox"
                      checked={boothForm.electricity}
                      onChange={(e) => setBoothForm({...boothForm, electricity: e.target.checked})}
                    />
                  </div>
                  <div className="form-group">
                    <label>Water Supply</label>
                    <input
                      type="checkbox"
                      checked={boothForm.water_supply}
                      onChange={(e) => setBoothForm({...boothForm, water_supply: e.target.checked})}
                    />
                  </div>
                  <div className="form-group">
                    <label>Outlets</label>
                    <input
                      type="number"
                      value={boothForm.outlets}
                      onChange={(e) => setBoothForm({...boothForm, outlets: parseInt(e.target.value) || 0})}
                    />
                  </div>
                </div>
                <button type="submit" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Booth'}
                </button>
              </form>
            )}

            {selectedEvent && (
              <div className="booths-list">
                {booths.map(booth => (
                  <div key={booth.booth_id} className="booth-item">
                    <div className="booth-info">
                      <h4>Booth {booth.booth_number}</h4>
                      <p>Size: {booth.size} | Price: ${booth.price}</p>
                      <p>Status: <span className={`status-${booth.status.toLowerCase()}`}>{booth.status}</span></p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Admin;