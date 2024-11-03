# python -m pytest
import sys
import pytest

sys.path.append('..')

from api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_save_experiment_file_success(client):
    response = client.post('/save_experiment_file', json={
        'yamlContent': 'example: value\nanother_example: value2',
        'filename': 'test.yaml'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "YAML file created successfully" in data['message']

def test_save_experiment_file_invalid_data(client):
    response = client.post('/save_experiment_file', json={})
    assert response.status_code == 400
    assert b"Invalid data" in response.data

def test_execute_success(client):
    response = client.post('/execute', json={
        'cmd': 'echo "Hello, World!"'
    })
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

def test_execute_invalid_command(client):
    response = client.post('/execute', json={
        'cmd': ''
    })
    assert response.status_code == 400
    assert b"Invalid command" in response.data

def test_cancel_no_process(client):
    response = client.post('/cancel')
    data = response.get_json()
    assert response.status_code == 404
    assert "No running process found" in data['status']

# Run with pytest in the terminal
