from fastapi import FastAPI, HTTPException

app = FastAPI()

# Data
employees = [
    {"id": 1, "name": "Kartik Malhotra", "age": 20, "department": "IT"},
    {"id": 2, "name": "Avi Malhotra", "age": 19, "department": "Testing"},
]


# GET METHOD TO RETRIEVE EVERY EMPLOYEE INFORMATION
@app.get("/", response_model=list)
def get_employees():
    return employees


# GET METHOD TO RETRIEVE EVERY EMPLOYEE INFORMATION
@app.get("/employees", response_model=list)
def get_employees():
    return employees


# GET METHOD USING EMPLOYEE ID TO RETRIEVE A SINGLE EMPLOYEE INFORMATION
@app.get("/employees/{employee_id}", response_model=dict)
def get_employee_by_id(employee_id: int):
    employee = next((i for i in employees if i["id"] == employee_id), None)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


# POST METHOD TO CREATE A NEW EMPLOYEE
@app.post("/employees", response_model=dict, status_code=201)
def create_employee(employee_data: dict):
    new_employee = {
        "id": len(employees) + 1,
        "name": employee_data["name"],
        "age": employee_data["age"],
        "department": employee_data["department"]
    }
    employees.append(new_employee)
    return {"message": "Employee created successfully"}


# PUT METHOD TO UPDATE INFORMATION FOR A SINGLE EMPLOYEE BY ACCESSING ITS ID
@app.put("/employees/{employee_id}", response_model=dict)
def update_employee(employee_id: int, employee_data: dict):
    employee = next((i for i in employees if i["id"] == employee_id), None)
    if employee:
        employee["name"] = employee_data["name"]
        employee["age"] = employee_data["age"]
        employee["department"] = employee_data["department"]
        return {"message": "Employee updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")
