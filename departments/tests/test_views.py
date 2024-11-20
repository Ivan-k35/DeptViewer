import pytest
from django.urls import reverse
from django.test.utils import override_settings
from departments.models import Department


@pytest.fixture
def use_locmem_cache():
    with override_settings(CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'OPTIONS': {
                'MAX_ENTRIES': 100,
            },
        }
    }):
        yield


@pytest.mark.django_db()
def test_department_tree_view(client, use_locmem_cache):
    Department.objects.create(name="IT Department")

    url = reverse('departments:department_tree')
    response = client.get(url)

    assert response.status_code == 200
    assert "IT Department" in response.content.decode()
