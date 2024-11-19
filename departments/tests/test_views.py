import pytest
from django.urls import reverse
from departments.models import Department


@pytest.mark.django_db
def test_department_tree_view(client):
    Department.objects.create(name="IT Department")

    url = reverse('departments:department_tree')
    response = client.get(url)

    assert response.status_code == 200
    assert "IT Department" in response.content.decode()
