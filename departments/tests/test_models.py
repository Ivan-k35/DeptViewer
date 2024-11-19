import pytest
from departments.models import Department, Employee


@pytest.mark.django_db
def test_department_creation():
    department = Department.objects.create(name="IT Department")
    assert department.name == "IT Department"


@pytest.mark.django_db
def test_employee_creation():
    department = Department.objects.create(name="HR")
    employee = Employee.objects.create(
        full_name="John Doe",
        position="Manager",
        hire_date="2024-01-01",
        salary=50000.00,
        department=department,
    )
    assert employee.full_name == "John Doe"
    assert employee.department.name == "HR"
