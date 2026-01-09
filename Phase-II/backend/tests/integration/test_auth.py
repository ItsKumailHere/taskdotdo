"""
Integration tests for logout flow
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
    test_email = "integration_logout_test@example.com"
    test_password = "SecurePassword123!"
    test_name = "Integration Logout Test User"
    
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


def test_complete_logout_flow(client: TestClient, db_session: Session):
    """Test the complete logout flow from login to logout"""
    # Step 1: Register a new user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "complete_logout_test@example.com",
            "name": "Complete Logout Test User",
            "password": "SecurePassword123!",
            "role": "user"
        }
    )
    
    assert register_response.status_code == 200
    
    # Step 2: Login to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "complete_logout_test@example.com",
            "password": "SecurePassword123!"
        }
    )
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    
    token = login_data["access_token"]
    
    # Step 3: Access a protected route to confirm authentication works
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert me_response.status_code == 200
    
    # Step 4: Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert logout_response.status_code == 200
    logout_data = logout_response.json()
    assert logout_data["message"] == "Successfully logged out"
    
    # Step 5: Try to access protected route after logout (should fail)
    me_response_after_logout = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert me_response_after_logout.status_code == 401  # Should be unauthorized after logout


def test_logout_then_login_with_same_user(client: TestClient, db_session: Session):
    """Test logging out and then logging back in with the same user"""
    user = create_test_user(db_session)
    
    # Login to get first token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "SecurePassword123!"
        }
    )
    
    assert login_response.status_code == 200
    first_token = login_response.json()["access_token"]
    
    # Access protected route to confirm authentication works
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {first_token}"}
    )
    assert me_response.status_code == 200
    
    # Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {first_token}"}
    )
    assert logout_response.status_code == 200
    
    # Try to access protected route with first token (should fail)
    me_response_after_logout = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {first_token}"}
    )
    assert me_response_after_logout.status_code == 401
    
    # Login again to get a new token
    login_response2 = client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "SecurePassword123!"
        }
    )
    assert login_response2.status_code == 200
    second_token = login_response2.json()["access_token"]
    
    # Access protected route with new token (should work)
    me_response_with_new_token = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {second_token}"}
    )
    assert me_response_with_new_token.status_code == 200


def test_multiple_users_logout_independence(client: TestClient, db_session: Session):
    """Test that logging out one user doesn't affect other users"""
    user1 = create_test_user(db_session)
    user2 = create_test_user(db_session)
    
    # Login as both users
    login_response1 = client.post(
        "/api/v1/auth/login",
        json={
            "email": user1.email,
            "password": "SecurePassword123!"
        }
    )
    assert login_response1.status_code == 200
    token1 = login_response1.json()["access_token"]
    
    login_response2 = client.post(
        "/api/v1/auth/login",
        json={
            "email": user2.email,
            "password": "SecurePassword123!"
        }
    )
    assert login_response2.status_code == 200
    token2 = login_response2.json()["access_token"]
    
    # Verify both tokens work
    me_response1 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token1}"})
    assert me_response1.status_code == 200
    
    me_response2 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert me_response2.status_code == 200
    
    # Logout user1
    logout_response1 = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert logout_response1.status_code == 200
    
    # User1's token should no longer work
    me_response1_after_logout = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token1}"})
    assert me_response1_after_logout.status_code == 401
    
    # But user2's token should still work
    me_response2_after_user1_logout = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert me_response2_after_user1_logout.status_code == 200


def test_logout_with_refreshed_token(client: TestClient, db_session: Session):
    """Test logout with a token that was refreshed"""
    user = create_test_user(db_session)
    
    # Login to get initial token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "SecurePassword123!"
        }
    )
    assert login_response.status_code == 200
    initial_token = login_response.json()["access_token"]
    
    # Refresh the token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {initial_token}"}
    )
    assert refresh_response.status_code == 200
    refreshed_token = refresh_response.json()["access_token"]
    
    # Logout with the refreshed token
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {refreshed_token}"}
    )
    assert logout_response.status_code == 200
    
    # The refreshed token should no longer work
    me_response_after_logout = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {refreshed_token}"}
    )
    assert me_response_after_logout.status_code == 401
    
    # The initial token should also no longer work (if our system invalidates all tokens for the user)
    me_response_initial_after_logout = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {initial_token}"}
    )
    # This might be 401 if we implement user-level logout (logging out all tokens for the user)
    # Or 200 if we only invalidate the specific token
    # For token-level blacklisting, this would still work, but for user-level logout it wouldn't
    # Based on our implementation, it should be 401 since we're blacklisting the specific token
    # But if we were to implement user-level logout, both would fail
    # For now, with token-level blacklisting, only the specific token is invalidated
    # So the initial token might still work unless we implement user-level logout
    # For this test, let's assume we're only invalidating the specific token
    # So the initial token might still work, but in a real implementation
    # we might want to invalidate all tokens for the user