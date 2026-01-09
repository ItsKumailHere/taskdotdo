"""
Contract tests for logout endpoint
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.models.user import User, get_password_hash
from app.database.session import engine
from uuid import uuid4
from datetime import datetime
from datetime import timedelta
from jose import jwt
import os


@pytest.fixture
def client():
    """Create a test client for the API"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Create a database session for testing"""
    with Session(engine) as session:
        yield session


def create_test_user(db_session: Session) -> User:
    """Helper function to create a test user"""
    test_email = "logout_test@example.com"
    test_password = "SecurePassword123!"
    test_name = "Logout Test User"
    
    # Hash the password
    hashed_password = get_password_hash(test_password)
    
    # Create user in database
    user = User(
        id=uuid4(),
        email=test_email,
        name=test_name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


def create_valid_token(user: User) -> str:
    """Helper function to create a valid JWT token"""
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def test_logout_endpoint_contract(client: TestClient, db_session: Session):
    """Test the contract of the logout endpoint"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    # Test logout with valid token
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Successfully logged out"


def test_logout_endpoint_without_token(client: TestClient):
    """Test logout without providing a token"""
    response = client.post("/api/v1/auth/logout")
    
    assert response.status_code == 403  # Should require authentication


def test_logout_endpoint_with_invalid_token(client: TestClient):
    """Test logout with an invalid token"""
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401  # Unauthorized


def test_access_protected_route_after_logout(client: TestClient, db_session: Session):
    """Test that accessing protected routes fails after logout"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    # Logout first
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_response.status_code == 200
    
    # Try to access protected route with the same token
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Should fail since token is now blacklisted
    assert me_response.status_code == 401


def test_logout_endpoint_idempotency(client: TestClient, db_session: Session):
    """Test that logout is idempotent - calling it multiple times should work"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    # Logout first time
    response1 = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response1.status_code == 200
    
    # Logout second time with same token (should still succeed)
    response2 = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 200