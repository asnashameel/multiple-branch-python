from main import app

def test_hello():
    app.testing = True  # Enable testing mode
    
    with app.test_client() as client:
        response = client.get('/')
        
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'Hello world with Flask'
