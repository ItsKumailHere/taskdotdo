"""
Integration tests for protected endpoints
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
    test_email = "integration_test@example.com"
    test_password = "SecurePassword123!"
    test_name = "Integration Test User"
    
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


def test_full_authentication_flow(client: TestClient, db_session: Session):
    """Test the complete authentication flow with protected endpoints"""
    # Step 1: Register a new user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "full_flow_test@example.com",
            "name": "Full Flow Test User",
            "password": "SecurePassword123!",
            "role": "user"
        }
    )
    
    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["email"] == "full_flow_test@example.com"
    
    # Step 2: Login to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "full_flow_test@example.com",
            "password": "SecurePassword123!"
        }
    )
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
    
    token = login_data["access_token"]
    
    # Step 3: Access protected /me endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "full_flow_test@example.com"
    
    # Step 4: Access protected user endpoint
    user_response = client.get(
        f"/api/v1/users/{me_data['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert user_response.status_code == 200
    user_data = user_response.json()
    assert user_data["id"] == me_data["id"]
    
    # Step 5: Refresh the token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert "access_token" in refresh_data
    assert refresh_data["token_type"] == "bearer"
    assert refresh_data["access_token"] != token  # New token should be different
    
    # Step 6: Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {refresh_data['access_token']}"}
    )
    
    assert logout_response.status_code == 200
    logout_data = logout_response.json()
    assert logout_data["message"] == "Successfully logged out"


def test_access_protected_endpoints_with_token(client: TestClient, db_session: Session):
    """Test accessing multiple protected endpoints with a valid token"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    # Test /me endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    
    # Test user endpoint
    user_response = client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert user_response.status_code == 200
    
    # Test refresh endpoint
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert refresh_response.status_code == 200
    
    # Test logout endpoint
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_response.status_code == 200


def test_access_protected_endpoints_without_token(client: TestClient):
    """Test that accessing protected endpoints without a token fails"""
    endpoints = [
        "/api/v1/auth/me",
        f"/api/v1/users/test-user-id",
        "/api/v1/auth/refresh",
        "/api/v1/auth/logout"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        # Most should return 403 (Forbidden) or 401 (Unauthorized)
        assert response.status_code in [401, 403], f"Endpoint {endpoint} should require authentication"


def test_cross_endpoint_authorization(client: TestClient, db_session: Session):
    """Test that users can only access their own data"""
    user1 = create_test_user(db_session)
    user2 = create_test_user(db_session)
    
    token1 = create_valid_token(user1)
    token2 = create_valid_token(user2)
    
    # User 1 should be able to access their own data
    response1 = client.get(
        f"/api/v1/users/{user1.id}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response1.status_code == 200
    
    # User 1 should NOT be able to access User 2's data
    response2 = client.get(
        f"/api/v1/users/{user2.id}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response2.status_code == 403  # Forbidden


def test_token_refresh_maintains_permissions(client: TestClient, db_session: Session):
    """Test that refreshed tokens maintain the same permissions"""
    user = create_test_user(db_session)
    original_token = create_valid_token(user)
    
    # Refresh the token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {original_token}"}
    )
    assert refresh_response.status_code == 200
    
    new_token = refresh_response.json()["access_token"]
    
    # Both tokens should allow access to protected endpoints
    for token in [original_token, new_token]:
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(user.id)


def test_concurrent_access_with_same_token(client: TestClient, db_session: Session):
    """Test that the same token can be used for concurrent requests"""
    user = create_test_user(db_session)
    token = create_valid_token(user)
    
    import threading
    import time
    
    results = []
    
    def make_request():
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        results.append(response.status_code)
    
    # Create multiple threads to simulate concurrent access
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # All requests should succeed
    assert all(status == 200 for status in results)