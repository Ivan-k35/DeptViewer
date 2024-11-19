import pytest
from departments.views import build_tree
from departments.models import Department, Employee


@pytest.mark.django_db
def test_build_tree():
    root = Department.objects.create(name="Head Office")
    child = Department.objects.create(name="Branch Office", parent=root)

    Employee.objects.create(full_name="Alice", position="CEO", hire_date="2024-01-01", salary=100000, department=root)
    Employee.objects.create(full_name="Bob", position="Manager", hire_date="2024-05-01", salary=50000, department=child)

    departments = Department.objects.all()
    tree = build_tree(departments)

    assert len(tree) == 1
    assert tree[0]["name"] == "Head Office"
    assert len(tree[0]["employees"]) == 1
    assert tree[0]["employees"][0]["full_name"] == "Alice"
    assert len(tree[0]["children"]) == 1
    assert tree[0]["children"][0]["name"] == "Branch Office"
