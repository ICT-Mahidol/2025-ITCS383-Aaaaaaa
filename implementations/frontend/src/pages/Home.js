import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');

  return (
    <div className="home">
      <div className="hero-section">
        <h1>Welcome to Booth Organizer System</h1>
        <p>Find and reserve booths for your favorite events</p>

        {!token ? (
          <div className="hero-actions">
            <Link to="/register" className="btn-primary">Get Started</Link>
            <Link to="/login" className="btn-secondary">Login</Link>
          </div>
        ) : (
          <div className="hero-actions">
            <Link to="/events" className="btn-primary">Browse Events</Link>
            {userRole === 'BOOTH_MANAGER' && (
              <Link to="/admin" className="btn-secondary">Admin Panel</Link>
            )}
          </div>
        )}
      </div>

      <div className="features-section">
        <h2>Why Choose Our Platform?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Easy Booking</h3>
            <p>Simple and intuitive booth reservation process</p>
          </div>
          <div className="feature-card">
            <h3>Multiple Events</h3>
            <p>Access to various events and exhibitions</p>
          </div>
          <div className="feature-card">
            <h3>Secure Payments</h3>
            <p>Safe and secure payment processing</p>
          </div>
          <div className="feature-card">
            <h3>Real-time Updates</h3>
            <p>Get instant notifications about your reservations</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;