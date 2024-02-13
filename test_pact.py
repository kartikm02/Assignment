from pact import Consumer, Provider
from fastapi.testclient import TestClient
from employee_api import app

# import pytest


# Create Pact consumer and provider instances
dashboard_consumer = Consumer('DashboardService')
employee_provider = Provider('EmployeeService')

# Ensure you have a valid Consumer instance
dashboard_consumer = dashboard_consumer.has_pact_with(
    employee_provider,
    port=8000  # Specify the actual port of your EmployeeService
)

# Define contracts without using upon_receiving
dashboard_contract_get = (dashboard_consumer
                          .given('A request for employee data')
                          .with_request('GET', '/dashboard/get_employee_data')
                          .will_respond_with(200, body={
    "name": "Kartik Malhotra",
    "age": 20,
    "department": "IT",
})
                          )

dashboard_contract_create = (dashboard_consumer
                             .given('A request to create employee data')
                             .with_request('POST', '/dashboard/create_employee_data')
                             .will_respond_with(201, body={"message": "Employee created successfully"})
                             )

dashboard_contract_update = (dashboard_consumer
                             .given('A request to update employee data')
                             .with_request('PUT',
                                           '/dashboard/update_employee_data/1')  # Update the employee_id for testing
                             .will_respond_with(200, body={"message": "Employee updated successfully"})
                             )

# Register contracts
dashboard_consumer.register_consumer_contract(dashboard_contract_get)
dashboard_consumer.register_consumer_contract(dashboard_contract_create)
dashboard_consumer.register_consumer_contract(dashboard_contract_update)


# Define test functions
def test_get_employee_data():
    with TestClient(app) as client:
        response = client.get("/dashboard/get_employee_data")
        assert response.status_code == 200
        assert response.json() == {"name": "Kartik Malhotra", "age": 20, "department": "IT"}


def test_create_employee_data():
    with TestClient(app) as client:
        data = {"name": "XYZ", "age": 19, "department": "Marketing"}
        response = client.post("/dashboard/create_employee_data", json=data)
        assert response.status_code == 201
        assert response.json() == {"message": "Employee created successfully"}


def test_update_employee_data():
    with TestClient(app) as client:
        data = {"name": "Updated Name", "age": 20, "department": "IT"}
        response = client.put("/dashboard/update_employee_data/1", json=data)
        assert response.status_code == 200
        assert response.json() == {"message": "Employee updated successfully"}

# try:
#     dashboard_consumer.verify()
# except Exception as e:
#     pytest.fail(f"Contract verification failed: {e}")
