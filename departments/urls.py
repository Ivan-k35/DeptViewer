from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('department_tree/', views.department_tree, name='department_tree'),
]
