from fastapi import FastAPI
from starlette.testclient import TestClient
from employee_api import app as employee_app

app = FastAPI()
client = TestClient(employee_app)

class DashboardService:
    def __init__(self, employee_service_base_url):
        self.employee_service_base_url = employee_service_base_url
    def get_employee_data(self):
        # Simulate a GET request to Employee Service
        # Assume the actual implementation makes an HTTP request
        response = client.get(f"{self.employee_service_base_url}/employees")
        return response.json()
    def create_employee_data(self, employee_data):
        # Simulate a POST request to Employee Service
        # Assume the actual implementation makes an HTTP request
        response = client.post(f"{self.employee_service_base_url}/employees", json=employee_data)
        return response.json()
    def update_employee_data(self, employee_id, employee_data):
        # Simulate a PUT request to Employee Service
        # Assume the actual implementation makes an HTTP request
        response = client.put(f"{self.employee_service_base_url}/employees/{employee_id}", json=employee_data)
        return response.json()

app.dashboard_service = DashboardService(employee_service_base_url="http://127.0.0.1:8000")

@app.get("/dashboard/get_employee_data", response_model=dict)
def get_employee_data():
    return app.dashboard_service.get_employee_data()

@app.post("/dashboard/create_employee_data", response_model=dict, status_code=201)
def create_employee_data(employee_data: dict):
    return app.dashboard_service.create_employee_data(employee_data)

@app.put("/dashboard/update_employee_data/{employee_id}", response_model=dict)
def update_employee_data(employee_id: int, employee_data: dict):
    return app.dashboard_service.update_employee_data(employee_id, employee_data)
