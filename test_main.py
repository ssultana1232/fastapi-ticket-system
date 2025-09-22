import pytest
from fastapi.testclient import TestClient
from main import api

client = TestClient(api)

# Clear tickets before each test
@pytest.fixture(autouse=True)
def clear_tickets():
    from main import tickets
    tickets.clear()
    yield
    tickets.clear()

def test_index():
    """Test the welcome message endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_get_tickets_empty():
    """Test getting tickets when list is empty"""
    response = client.get("/ticket")
    assert response.status_code == 200
    assert response.json() == []

def test_add_ticket():
    """Test adding a new ticket"""
    ticket_data = {
        "id": 1,
        "flight_name": "AI101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data

def test_get_tickets_with_data():
    """Test getting tickets when data exists"""
    # First add a ticket
    ticket_data = {
        "id": 1,
        "flight_name": "AI101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=ticket_data)
    
    # Then get tickets
    response = client.get("/ticket")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == ticket_data

def test_update_ticket():
    """Test updating an existing ticket"""
    # First add a ticket
    original_ticket = {
        "id": 1,
        "flight_name": "AI101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=original_ticket)
    
    # Update the ticket
    updated_ticket = {
        "id": 1,
        "flight_name": "AI102",
        "flight_date": "2025-10-16",
        "flight_time": "16:30",
        "destination": "London"
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket

def test_update_nonexistent_ticket():
    """Test updating a ticket that doesn't exist"""
    ticket_data = {
        "id": 999,
        "flight_name": "AI999",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Paris"
    }
    response = client.put("/ticket/999", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket Not Found"}

def test_delete_ticket():
    """Test deleting an existing ticket"""
    # First add a ticket
    ticket_data = {
        "id": 1,
        "flight_name": "AI101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=ticket_data)
    
    # Delete the ticket
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json() == ticket_data
    
    # Verify it's deleted
    get_response = client.get("/ticket")
    assert len(get_response.json()) == 0

def test_delete_nonexistent_ticket():
    """Test deleting a ticket that doesn't exist"""
    response = client.delete("/ticket/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}

def test_multiple_tickets():
    """Test adding and managing multiple tickets"""
    tickets_data = [
        {
            "id": 1,
            "flight_name": "AI101",
            "flight_date": "2025-10-15",
            "flight_time": "14:30",
            "destination": "New York"
        },
        {
            "id": 2,
            "flight_name": "AI102",
            "flight_date": "2025-10-16",
            "flight_time": "16:30",
            "destination": "London"
        }
    ]
    
    # Add multiple tickets
    for ticket in tickets_data:
        response = client.post("/ticket", json=ticket)
        assert response.status_code == 200
    
    # Get all tickets
    response = client.get("/ticket")
    assert response.status_code == 200
    assert len(response.json()) == 2