import pytest
import requests
import allure
import jsonschema

BASE_URL = "https://jsonplaceholder.typicode.com/posts"  # Example API endpoint
SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["userId", "id", "title", "body"]
}

@allure.feature("API Testing")
@allure.story("Validate REST API Endpoints")
def test_get_request():
    response = requests.get(BASE_URL)
    allure.attach(response.text, name="GET Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200, "GET request failed"
    assert isinstance(response.json(), list), "Response is not a list"
    
    # Validate JSON Schema for the first item
    if response.json():
        jsonschema.validate(instance=response.json()[0], schema=SCHEMA)

@allure.story("Validate POST Request")
def test_post_request():
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(BASE_URL, json=payload)
    allure.attach(response.text, name="POST Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 201, "POST request failed"
    assert response.json()["title"] == "foo", "Title mismatch in POST response"
    jsonschema.validate(instance=response.json(), schema=SCHEMA)

@allure.story("Validate PUT Request")
def test_put_request():
    payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}
    response = requests.put(f"{BASE_URL}/1", json=payload)
    allure.attach(response.text, name="PUT Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200, "PUT request failed"
    assert response.json()["title"] == "updated title", "Title not updated"
    jsonschema.validate(instance=response.json(), schema=SCHEMA)

@allure.story("Validate DELETE Request")
def test_delete_request():
    response = requests.delete(f"{BASE_URL}/1")
    allure.attach(response.text, name="DELETE Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code == 200, "DELETE request failed"

@allure.story("Authentication Test - API Key")
def test_api_key_auth():
    headers = {"Authorization": "Bearer your_api_key_here"}  # Replace with actual key
    response = requests.get(BASE_URL, headers=headers)
    allure.attach(response.text, name="API Key Auth Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code in [200, 401], "Unexpected response for API key auth"

@allure.story("Authentication Test - OAuth2")
def test_oauth_auth():
    token = "your_oauth_token_here"  # Replace with actual token
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(BASE_URL, headers=headers)
    allure.attach(response.text, name="OAuth2 Auth Response", attachment_type=allure.attachment_type.JSON)
    assert response.status_code in [200, 401], "Unexpected response for OAuth2 auth"

if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])