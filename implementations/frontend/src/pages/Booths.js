import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { boothService, reservationService } from '../services/api';
import BoothCard from '../components/BoothCard';
import './Booths.css';

const Booths = () => {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const [booths, setBooths] = useState([]);
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedBooth, setSelectedBooth] = useState(null);

  useEffect(() => {
    fetchBooths();
  }, [eventId]);

  const fetchBooths = async () => {
    try {
      const response = await boothService.getBoothsByEvent(eventId);
      setBooths(response.data);
      // For now, we'll assume event info is available or fetch it separately
      setEvent({ name: `Event ${eventId}` }); // Placeholder
    } catch (err) {
      setError('Failed to load booths');
    } finally {
      setLoading(false);
    }
  };

  const handleReserveBooth = async (booth) => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      await reservationService.createReservation({
        booth_id: booth.booth_id,
        reservation_type: booth.duration_type
      });

      // Update booth status locally
      setBooths(booths.map(b =>
        b.booth_id === booth.booth_id
          ? { ...b, status: 'RESERVED' }
          : b
      ));

      alert('Booth reserved successfully!');
    } catch (err) {
      alert('Failed to reserve booth: ' + (err.response?.data?.detail || 'Unknown error'));
    }
  };

  if (loading) {
    return <div className="loading">Loading booths...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="booths-page">
      <div className="page-header">
        <h1>{event?.name} - Available Booths</h1>
        <p>Select a booth to reserve for this event</p>
      </div>

      <div className="booths-grid">
        {booths.length === 0 ? (
          <div className="no-booths">
            <h3>No booths available</h3>
            <p>All booths for this event have been reserved</p>
          </div>
        ) : (
          booths.map(booth => (
            <BoothCard
              key={booth.booth_id}
              booth={booth}
              onReserve={handleReserveBooth}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Booths;