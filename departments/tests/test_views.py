import pytest
from django.urls import reverse
from django.core.cache import cache
from departments.models import Department


@pytest.mark.django_db(transaction=True)
def test_department_tree_view(client):
    Department.objects.create(name="IT Department")
    cache.delete('department_tree_data')

    url = reverse('departments:department_tree')
    response = client.get(url)

    assert response.status_code == 200
    assert "IT Department" in response.content.decode()
    cache.delete('department_tree_data')
