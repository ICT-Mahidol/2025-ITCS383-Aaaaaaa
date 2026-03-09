import pytest
from app.services.auth_service import (
    verify_password, get_password_hash, authenticate_user,
    create_user, get_user_by_username
)
from app.schemas.user_schema import UserCreate
from app.models.user import UserRole
from tests.factories import UserFactory

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_user(db_session):
    user_data = UserCreate(
        username="testuser",
        password="testpass",
        name="Test User",
        citizen_id="1234567890123",
        contact_info="test@example.com",
        role=UserRole.MERCHANT
    )
    user = create_user(db_session, user_data)

    assert user.username == "testuser"
    assert user.name == "Test User"
    assert user.role == UserRole.MERCHANT
    assert not verify_password("wrongpass", user.password)

def test_authenticate_user(db_session):
    # Create a user
    user_data = UserCreate(
        username="authuser",
        password="authpass",
        name="Auth User",
        role=UserRole.GENERAL_USER
    )
    created_user = create_user(db_session, user_data)

    # Test successful authentication
    authenticated = authenticate_user(db_session, "authuser", "authpass")
    assert authenticated is not None
    assert authenticated.username == "authuser"

    # Test failed authentication
    failed = authenticate_user(db_session, "authuser", "wrongpass")
    assert failed is None

def test_get_user_by_username(db_session):
    user = UserFactory(username="uniqueuser")
    db_session.add(user)
    db_session.commit()

    found_user = get_user_by_username(db_session, "uniqueuser")
    assert found_user is not None
    assert found_user.username == "uniqueuser"

    not_found = get_user_by_username(db_session, "nonexistent")
    assert not_found is None