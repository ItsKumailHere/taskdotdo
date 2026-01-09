"""
Contract tests for JWT token validation middleware
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.models.user import User, get_password_hash
from app.database.session import engine
from uuid import uuid4
from datetime import datetime, timedelta
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
    test_email = "jwt_test@example.com"
    test_password = "SecurePassword123!"
    test_name = "JWT Test User"
    
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


def create_expired_token(user: User) -> str:
    """Helper function to create an expired JWT token"""
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "exp": datetime.utcnow() - timedelta(minutes=30)  # Expired token
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def test_protected_route_with_valid_token(client: TestClient, db_session: Session):
    """Test accessing a protected route with a valid JWT token"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    # Test accessing the /me endpoint with a valid token
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "id" in data
    assert data["email"] == user.email
    assert data["name"] == user.name


def test_protected_route_without_token(client: TestClient, db_session: Session):
    """Test accessing a protected route without a JWT token"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 403  # Unauthorized - token required


def test_protected_route_with_invalid_token(client: TestClient):
    """Test accessing a protected route with an invalid JWT token"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401  # Unauthorized - invalid token


def test_protected_route_with_expired_token(client: TestClient, db_session: Session):
    """Test accessing a protected route with an expired JWT token"""
    user = create_test_user(db_session)
    expired_token = create_expired_token(user)
    
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401  # Unauthorized - expired token


def test_refresh_token_endpoint(client: TestClient, db_session: Session):
    """Test the token refresh endpoint"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify the new token is different from the old one
    assert data["access_token"] != token


def test_refresh_token_with_invalid_token(client: TestClient):
    """Test refreshing a token with an invalid JWT token"""
    response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401  # Unauthorized - invalid token


def test_logout_endpoint(client: TestClient, db_session: Session):
    """Test the logout endpoint"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "message" in data
    assert data["message"] == "Successfully logged out"


def test_get_user_endpoint(client: TestClient, db_session: Session):
    """Test the get user endpoint with proper authentication"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    response = client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["name"] == user.name