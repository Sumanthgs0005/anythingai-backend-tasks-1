import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Health Check Tests
def test_health_check():
    """Test API health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Authentication Tests
class TestAuthentication:
    """Test user authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "testuser@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails"""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        assert response.status_code == 400
    
    def test_login_user(self):
        """Test user login"""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "pass123"
            }
        )
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "pass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

# Task Tests
class TestTasks:
    """Test task management endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and authentication token"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "taskuser@example.com",
                "password": "pass123"
            }
        )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_create_task(self):
        """Test creating a task"""
        response = client.post(
            "/api/v1/tasks/",
            headers=self.headers,
            json={
                "title": "Test Task",
                "description": "A test task"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
    
    def test_get_tasks(self):
        """Test getting all tasks"""
        response = client.get(
            "/api/v1/tasks/",
            headers=self.headers
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_task_unauthorized(self):
        """Test creating task without authentication"""
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "A test task"
            }
        )
        assert response.status_code == 401
