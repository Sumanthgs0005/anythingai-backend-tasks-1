from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.post(
    "/api/v1/auth/register",
    json={"email": "taskuser@example.com", "password": "pass123"},
)
print("STATUS:", response.status_code)
print("BODY:", response.text)
print("JSON:", None if not response.content else response.json())
