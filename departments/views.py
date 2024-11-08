from django.shortcuts import render
from django.core.cache import cache
from loguru import logger
from .models import Department


def build_tree(departments):
    """
        Построение иерархического дерева подразделений и сотрудников.

        :param departments: QuerySet с подразделениями.
        :return: Список словарей, представляющий дерево подразделений.
    """

    def recurse(dept):
        return {
            "id": dept.id,
            "name": dept.name,
            "employees": [
                {
                    "id": emp.id,
                    "full_name": emp.full_name,
                    "position": emp.position,
                    "date_of_hire": emp.hire_date.strftime("%Y-%m-%d"),
                    "salary": str(emp.salary),
                } for emp in dept.employees.all()
            ],
            "children": [recurse(child) for child in dept.get_children()]
        }

    return [recurse(dept) for dept in departments if dept.is_root_node()]


def department_tree(request):
    """
        Представление для отображения дерева департаментов и их сотрудников.

        :param request: HTTP-запрос
        :return: HTTP-ответ с шаблоном и данными дерева.
    """
    try:
        tree_data = cache.get('department_tree_data')

        if not tree_data:
            departments = Department.objects.prefetch_related('employees').all()
            tree_data = build_tree(departments)
            cache.set('department_tree_data', tree_data, 60)

        return render(request, 'departments/department_tree.html',
                      {'tree_data': tree_data})

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных департаментов: {e}")
        return render(request, 'departments/error.html',
                      {"message": "Сервис временно недоступен, попробуйте позже."})
