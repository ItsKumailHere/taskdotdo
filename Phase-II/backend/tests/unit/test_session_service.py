"""
Unit tests for session invalidation functionality
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.auth_service import logout_user, is_token_blacklisted, token_blacklist


@pytest.fixture(autouse=True)
def clear_token_blacklist():
    """Clear the token blacklist before each test"""
    token_blacklist.clear()


@pytest.mark.asyncio
async def test_logout_user_adds_token_to_blacklist():
    """Test that logout_user adds the token to the blacklist"""
    # Create a mock user
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    
    test_token = "test.jwt.token"
    
    # Call the logout function
    result = await logout_user(mock_user, test_token)
    
    # Verify the function returns True (success)
    assert result is True
    
    # Verify the token was added to the blacklist
    assert test_token in token_blacklist


@pytest.mark.asyncio
async def test_logout_user_multiple_tokens():
    """Test that multiple tokens can be added to the blacklist"""
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    
    token1 = "test.jwt.token.1"
    token2 = "test.jwt.token.2"
    
    # Logout with first token
    result1 = await logout_user(mock_user, token1)
    assert result1 is True
    assert token1 in token_blacklist
    
    # Logout with second token
    result2 = await logout_user(mock_user, token2)
    assert result2 is True
    assert token2 in token_blacklist
    assert len(token_blacklist) == 2


def test_is_token_blacklisted_when_token_is_blacklisted():
    """Test that is_token_blacklisted returns True for blacklisted tokens"""
    test_token = "blacklisted.token"
    token_blacklist.add(test_token)
    
    result = is_token_blacklisted(test_token)
    assert result is True


def test_is_token_blacklisted_when_token_is_not_blacklisted():
    """Test that is_token_blacklisted returns False for non-blacklisted tokens"""
    test_token = "not.blacklisted.token"
    
    result = is_token_blacklisted(test_token)
    assert result is False


def test_is_token_blacklisted_with_empty_blacklist():
    """Test that is_token_blacklisted returns False when blacklist is empty"""
    # Ensure blacklist is empty
    token_blacklist.clear()
    
    result = is_token_blacklisted("any.token")
    assert result is False


@pytest.mark.asyncio
async def test_logout_user_idempotency():
    """Test that logging out the same token multiple times works correctly"""
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    
    test_token = "test.jwt.token"
    
    # Logout the same token multiple times
    result1 = await logout_user(mock_user, test_token)
    result2 = await logout_user(mock_user, test_token)
    result3 = await logout_user(mock_user, test_token)
    
    # All should return True
    assert result1 is True
    assert result2 is True
    assert result3 is True
    
    # Token should still be in the blacklist (only once)
    assert test_token in token_blacklist
    assert len(token_blacklist) == 1


@pytest.mark.asyncio
async def test_logout_user_different_users():
    """Test that tokens from different users are handled correctly"""
    mock_user1 = MagicMock()
    mock_user1.id = "user-1-id"
    
    mock_user2 = MagicMock()
    mock_user2.id = "user-2-id"
    
    token1 = "user1.token"
    token2 = "user2.token"
    
    # Logout tokens from different users
    result1 = await logout_user(mock_user1, token1)
    result2 = await logout_user(mock_user2, token2)
    
    assert result1 is True
    assert result2 is True
    
    # Both tokens should be in the blacklist
    assert token1 in token_blacklist
    assert token2 in token_blacklist
    assert len(token_blacklist) == 2


def test_token_blacklist_persistence():
    """Test that the token blacklist persists between function calls"""
    token1 = "persistent.token.1"
    token2 = "persistent.token.2"
    
    # Add tokens to blacklist
    token_blacklist.add(token1)
    token_blacklist.add(token2)
    
    # Verify they're in the blacklist
    assert token1 in token_blacklist
    assert token2 in token_blacklist
    
    # Verify other tokens are not in the blacklist
    assert "other.token" not in token_blacklist


@pytest.mark.asyncio
async def test_logout_user_with_special_characters_in_token():
    """Test logout with tokens containing special characters"""
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    
    # Token with special characters
    special_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    result = await logout_user(mock_user, special_token)
    assert result is True
    assert special_token in token_blacklist