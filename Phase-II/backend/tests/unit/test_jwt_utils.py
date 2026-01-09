"""
Unit tests for JWT token validation utilities
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt
import os
from app.utils.jwt import create_access_token, verify_token, get_user_id_from_token, is_token_expired, refresh_access_token


def test_create_access_token():
    """Test creating an access token with default expiration"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data)
    
    # Verify the token was created
    assert token is not None
    assert isinstance(token, str)
    
    # Decode and verify the token contents
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_payload["sub"] == "test-user-id"
    assert decoded_payload["email"] == "test@example.com"
    assert "exp" in decoded_payload


def test_create_access_token_with_custom_expiration():
    """Test creating an access token with custom expiration time"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    custom_expiry = timedelta(minutes=10)
    token = create_access_token(data, expires_delta=custom_expiry)
    
    # Verify the token was created
    assert token is not None
    
    # Decode and verify the token expiration
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp_time = datetime.utcfromtimestamp(decoded_payload["exp"])
    expected_exp = datetime.utcnow() + custom_expiry
    
    # Allow for a small time difference
    assert abs((exp_time - expected_exp).total_seconds()) < 5


def test_verify_token_valid():
    """Test verifying a valid token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    
    assert payload is not None
    assert payload["sub"] == "test-user-id"
    assert payload["email"] == "test@example.com"


def test_verify_token_invalid():
    """Test verifying an invalid token"""
    payload = verify_token("invalid.token.string")
    
    assert payload is None


def test_verify_token_expired():
    """Test verifying an expired token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    # Create a token that expired 1 hour ago
    expired_time = datetime.utcnow() - timedelta(hours=1)
    token_data = {**data, "exp": expired_time}
    
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    payload = verify_token(token)
    
    assert payload is None


def test_get_user_id_from_token_valid():
    """Test extracting user ID from a valid token"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data)
    
    user_id = get_user_id_from_token(token)
    
    assert user_id == "test-user-id"


def test_get_user_id_from_token_invalid():
    """Test extracting user ID from an invalid token"""
    user_id = get_user_id_from_token("invalid.token.string")
    
    assert user_id is None


def test_is_token_expired_valid():
    """Test checking if a valid token is expired"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    token = create_access_token(data)
    
    expired = is_token_expired(token)
    
    assert expired is False


def test_is_token_expired_expired():
    """Test checking if an expired token is expired"""
    data = {"sub": "test-user-id", "email": "test@example.com"}
    # Create a token that expired 1 hour ago
    expired_time = datetime.utcnow() - timedelta(hours=1)
    token_data = {**data, "exp": expired_time}
    
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    expired = is_token_expired(token)
    
    assert expired is True


def test_is_token_expired_invalid():
    """Test checking if an invalid token is expired"""
    expired = is_token_expired("invalid.token.string")
    
    assert expired is True


def test_refresh_access_token_valid():
    """Test refreshing a valid token that is about to expire"""
    data = {"sub": "test-user-id", "email": "test@example.com", "role": "user"}
    # Create a token that expires in 2 minutes (soon)
    soon_to_expire = datetime.utcnow() + timedelta(minutes=2)
    token_data = {**data, "exp": soon_to_expire.timestamp()}
    
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    new_token = refresh_access_token(token)
    
    # Should return a new token since the original is about to expire
    assert new_token is not None
    assert new_token != token
    
    # Verify the new token has updated expiration
    new_payload = jwt.decode(new_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert new_payload["sub"] == "test-user-id"
    assert new_payload["email"] == "test@example.com"
    assert new_payload["role"] == "user"


def test_refresh_access_token_not_needed():
    """Test refreshing a valid token that is not close to expiring"""
    data = {"sub": "test-user-id", "email": "test@example.com", "role": "user"}
    token = create_access_token(data)
    
    # This token has a full 30-minute validity, so refresh shouldn't be needed
    new_token = refresh_access_token(token)
    
    # Should return None since the original token is still valid for a while
    assert new_token is None


def test_refresh_access_token_invalid():
    """Test refreshing an invalid token"""
    new_token = refresh_access_token("invalid.token.string")
    
    assert new_token is None


def test_refresh_access_token_expired():
    """Test refreshing an expired token"""
    data = {"sub": "test-user-id", "email": "test@example.com", "role": "user"}
    # Create a token that expired 1 hour ago
    expired_time = datetime.utcnow() - timedelta(hours=1)
    token_data = {**data, "exp": expired_time}
    
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    new_token = refresh_access_token(token)
    
    assert new_token is None