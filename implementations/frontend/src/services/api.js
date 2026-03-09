import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: (userData) => api.post('/api/auth/register', userData),
  login: (credentials) => api.post('/api/auth/login', credentials),
};

export const eventService = {
  getEvents: () => api.get('/api/events'),
  createEvent: (eventData) => api.post('/api/events', eventData),
  updateEvent: (eventId, eventData) => api.put(`/api/events/${eventId}`, eventData),
  deleteEvent: (eventId) => api.delete(`/api/events/${eventId}`),
};

export const boothService = {
  getBoothsByEvent: (eventId) => api.get(`/api/booths/event/${eventId}`),
  createBooth: (boothData) => api.post('/api/booths', boothData),
  updateBooth: (boothId, boothData) => api.put(`/api/booths/${boothId}`, boothData),
  deleteBooth: (boothId) => api.delete(`/api/booths/${boothId}`),
};

export const reservationService = {
  createReservation: (reservationData) => api.post('/api/reservations', reservationData),
  getUserReservations: () => api.get('/api/reservations'),
};

export const paymentService = {
  createPayment: (paymentData) => api.post('/api/payments', paymentData),
  uploadSlip: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/payments/upload-slip', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default api;