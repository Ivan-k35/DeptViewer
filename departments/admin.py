from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ("tree_actions", "indented_title",)
    list_display_links = ("indented_title",)
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "hire_date", "salary", "department")
    list_filter = ("department",)
    search_fields = ("full_name", "department__name")
    ordering = ("department", "hire_date")
