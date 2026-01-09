"""
Unit tests for authentication service
"""
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from app.services.auth_service import authenticate_user
from app.models.user import User, get_password_hash
from uuid import uuid4
from datetime import datetime


@pytest.mark.asyncio
async def test_authenticate_user_success():
    """Test successful user authentication"""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    
    # Create a test user
    test_email = "test@example.com"
    test_password = "SecurePassword123!"
    hashed_password = get_password_hash(test_password)
    
    test_user = User(
        id=uuid4(),
        email=test_email,
        name="Test User",
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    # Mock the exec method to return the test user
    mock_result = MagicMock()
    mock_result.first.return_value = test_user
    mock_session.exec.return_value = mock_result
    
    # Call the authenticate_user function
    result = await authenticate_user(mock_session, test_email, test_password)
    
    # Verify the result
    assert result is not None
    assert result.email == test_email


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    """Test authentication with wrong password"""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    
    # Create a test user
    test_email = "test@example.com"
    test_password = "SecurePassword123!"
    hashed_password = get_password_hash(test_password)
    
    test_user = User(
        id=uuid4(),
        email=test_email,
        name="Test User",
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    # Mock the exec method to return the test user
    mock_result = MagicMock()
    mock_result.first.return_value = test_user
    mock_session.exec.return_value = mock_result
    
    # Call the authenticate_user function with wrong password
    result = await authenticate_user(mock_session, test_email, "wrongpassword")
    
    # Verify the result is None
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_user_nonexistent_email():
    """Test authentication with non-existent email"""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    
    # Mock the exec method to return None (no user found)
    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_session.exec.return_value = mock_result
    
    # Call the authenticate_user function
    result = await authenticate_user(mock_session, "nonexistent@example.com", "anypassword")
    
    # Verify the result is None
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_user_empty_password():
    """Test authentication with empty password"""
    # Create a mock session
    mock_session = AsyncMock(spec=AsyncSession)
    
    # Create a test user
    test_email = "test@example.com"
    test_password = "SecurePassword123!"
    hashed_password = get_password_hash(test_password)
    
    test_user = User(
        id=uuid4(),
        email=test_email,
        name="Test User",
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    # Mock the exec method to return the test user
    mock_result = MagicMock()
    mock_result.first.return_value = test_user
    mock_session.exec.return_value = mock_result
    
    # Call the authenticate_user function with empty password
    result = await authenticate_user(mock_session, test_email, "")
    
    # Verify the result is None
    assert result is None