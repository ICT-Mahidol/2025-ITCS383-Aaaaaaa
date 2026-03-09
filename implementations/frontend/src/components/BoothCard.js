import React from 'react';
import './BoothCard.css';

const BoothCard = ({ booth, onReserve }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'AVAILABLE': return '#27ae60';
      case 'RESERVED': return '#f39c12';
      case 'OCCUPIED': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  return (
    <div className="booth-card">
      <div className="booth-header">
        <h4 className="booth-number">{booth.booth_number}</h4>
        <span
          className="booth-status"
          style={{ backgroundColor: getStatusColor(booth.status) }}
        >
          {booth.status}
        </span>
      </div>

      <div className="booth-details">
        <div className="booth-info">
          <span>Size: {booth.size}</span>
          <span>Type: {booth.type}</span>
          <span>Price: ${booth.price}</span>
        </div>

        <div className="booth-facilities">
          {booth.electricity && <span className="facility">⚡ Electricity</span>}
          {booth.water_supply && <span className="facility">💧 Water</span>}
          {booth.outlets > 0 && <span className="facility">🔌 {booth.outlets} Outlets</span>}
        </div>
      </div>

      {booth.status === 'AVAILABLE' && onReserve && (
        <button
          className="reserve-btn"
          onClick={() => onReserve(booth)}
        >
          Reserve Booth
        </button>
      )}
    </div>
  );
};

export default BoothCard;