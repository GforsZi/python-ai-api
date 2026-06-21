from pydantic import BaseModel
from app.shared.utils import ApiResponse

# Positif Cases

def test_api_response_success_format():
    response = ApiResponse(message="Success", data={"id": 1}, status_code=200)
    data = response.to_dict()
    assert data["success"] is True
    assert data["message"] == "Success"
    assert data["data"] == {"id": 1}
    assert data["status_code"] == 200

def test_api_response_with_pydantic_model():
    class UserSchema(BaseModel):
        username: str
        
    user = UserSchema(username="testuser")
    response = ApiResponse(message="User created", data=user, status_code=201)
    data = response.to_dict()
    assert data["data"] == {"username": "testuser"}
    assert data["success"] is True

# Negatif Cases

def test_api_response_failure_format():
    response = ApiResponse(message="Error", data=None, status_code=400)
    data = response.to_dict()
    assert data["success"] is False
    assert data["status_code"] == 400

def test_api_response_handles_none_values():
    response = ApiResponse(message="No Data", data=None, current_user=None, status_code=200)
    data = response.to_dict()
    assert data["data"] is None
    assert data["current_user"] is None
    assert data["success"] is True
