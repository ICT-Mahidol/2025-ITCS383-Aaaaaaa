from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db_connection import engine
from app.models import user, merchant, event, booth, reservation, payment
from app.routes import auth_routes, event_routes, booth_routes, reservation_routes, payment_routes

# Create database tables
user.Base.metadata.create_all(bind=engine)
merchant.Base.metadata.create_all(bind=engine)
event.Base.metadata.create_all(bind=engine)
booth.Base.metadata.create_all(bind=engine)
reservation.Base.metadata.create_all(bind=engine)
payment.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booth Organizer System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(event_routes.router, prefix="/api/events", tags=["Events"])
app.include_router(booth_routes.router, prefix="/api/booths", tags=["Booths"])
app.include_router(reservation_routes.router, prefix="/api/reservations", tags=["Reservations"])
app.include_router(payment_routes.router, prefix="/api/payments", tags=["Payments"])

@app.get("/")
def read_root():
    return {"message": "Booth Organizer System API"}