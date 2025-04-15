from starlette.testclient import TestClient
from server import app

def test_protected_route_redirect():
    client = TestClient(app)

    with client:
        # Make sure no session is present
        client.cookies.clear()

        response = client.get("/welcome")

        # Here it checks that the redirected page does not contain task content
        assert "Welcome," not in response.text
