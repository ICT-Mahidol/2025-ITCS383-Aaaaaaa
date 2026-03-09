# Testing

This directory contains unit tests for the Booth Organizer System backend.

## Setup

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_auth_service.py
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Test Structure

- `conftest.py`: Pytest fixtures for database setup
- `factories.py`: Factory Boy factories for creating test data
- `test_models.py`: Tests for database models
- `test_*_service.py`: Tests for business logic services
- `test_routes.py`: Tests for API endpoints

## Test Database

Tests use SQLite in-memory database for isolation and speed.