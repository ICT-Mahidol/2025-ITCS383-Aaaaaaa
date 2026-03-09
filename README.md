# Booth Organizer System

A full-stack web application for managing booth reservations at events. Built with FastAPI backend and React frontend.

## Architecture

### Backend (FastAPI + SQLAlchemy + MySQL)
- RESTful API with JWT authentication
- Role-based access control (General User, Merchant, Booth Manager)
- CRUD operations for events, booths, reservations, and payments
- Business logic for booth availability and reservation rules

### Frontend (React)
- Responsive single-page application
- User authentication and authorization
- Event browsing and booth selection
- Admin dashboard for booth managers

## Features

### For General Users & Merchants
- User registration and login
- Browse available events
- View booth details and availability
- Reserve booths with payment processing
- View reservation and payment status

### For Booth Managers
- Create and manage events
- Add and configure booths for events
- Approve merchant registrations
- Verify payments and manage reservations
- Generate reports

## Technology Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic, PyMySQL
- **Frontend**: React 18, React Router, Axios, CSS3
- **Database**: MySQL
- **Authentication**: JWT tokens
- **Testing**: pytest, Factory Boy

## Project Structure

```
implementations/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── database/
│   │   │   └── db_connection.py    # Database configuration
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── routes/                 # API endpoints
│   │   ├── services/               # Business logic
│   │   └── __init__.py
│   ├── tests/                      # Unit tests
│   ├── requirements.txt
│   ├── pytest.ini
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/             # Reusable React components
│   │   ├── pages/                  # Page components
│   │   ├── services/               # API service functions
│   │   └── App.js
│   ├── package.json
│   └── .env
└── database.sql                    # MySQL schema
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Git

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd implementations/backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database:**
   ```bash
   # Create MySQL database
   mysql -u root -p < ../database.sql
   ```

4. **Configure environment:**
   Edit `.env` file with your database credentials:
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/booth_system
   JWT_SECRET=your_secret_key_here
   ```

5. **Run backend:**
   ```bash
   uvicorn app.main:app --reload
   ```
   API available at: http://localhost:8000
   API docs at: http://localhost:8000/docs

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd implementations/frontend
   npm install
   ```

2. **Configure API URL:**
   The `.env` file is already configured for local development.

3. **Run frontend:**
   ```bash
   npm start
   ```
   App available at: http://localhost:3000

## Testing

### Backend Tests
```bash
cd implementations/backend
pip install -r requirements.txt
pytest tests/
```

### Frontend Tests
```bash
cd implementations/frontend
npm test
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create event (Booth Manager)
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event

### Booths
- `GET /api/booths/event/{event_id}` - Get booths for event
- `POST /api/booths` - Create booth
- `PUT /api/booths/{id}` - Update booth
- `DELETE /api/booths/{id}` - Delete booth

### Reservations
- `POST /api/reservations` - Create reservation
- `GET /api/reservations` - Get user reservations

### Payments
- `POST /api/payments` - Create payment
- `POST /api/payments/upload-slip` - Upload payment slip

## Business Rules

1. Users must register before reserving booths
2. Merchant accounts require booth manager approval
3. Citizen ID verification via MOI API (mocked)
4. Booth reservations require full payment
5. No installment payments allowed
6. Booth double booking is prevented
7. Reservations are confirmed only after payment approval

## Development Workflow

1. **Backend Development:**
   - Add models in `app/models/`
   - Create schemas in `app/schemas/`
   - Implement business logic in `app/services/`
   - Add API routes in `app/routes/`
   - Write unit tests in `tests/`

2. **Frontend Development:**
   - Create components in `src/components/`
   - Add pages in `src/pages/`
   - Update API calls in `src/services/`
   - Add routes in `App.js`

3. **Testing:**
   - Run backend tests: `pytest`
   - Run frontend tests: `npm test`

## Deployment

### Backend
- Use production WSGI server (gunicorn)
- Configure production database
- Set secure JWT secret
- Enable HTTPS

### Frontend
- Build production bundle: `npm run build`
- Serve static files with nginx/apache
- Configure API proxy for production API URL

## Future Enhancements

- Interactive booth map visualization
- Real-time availability updates
- Email/SMS notifications
- Admin analytics dashboard
- Mobile app development
- Multi-language support
- Payment gateway integrations