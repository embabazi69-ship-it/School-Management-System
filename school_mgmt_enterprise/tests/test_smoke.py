
from app import create_app
def test_index():
    app = create_app()
    client = app.test_client()
    r = client.get('/')
    assert r.status_code == 200
