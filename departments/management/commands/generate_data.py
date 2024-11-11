import random
from faker import Faker
from django.core.management.base import BaseCommand
from departments.models import Employee, Department
from loguru import logger

fake = Faker("ru_RU")


def generate_department_name(existing_names):
    base_names = ['Маркетинг', 'Разработка', 'Продажи', 'Финансы', 'HR', 'Логистика', 'Техническая поддержка',
                  'Аналитика']

    department_name = f"{random.choice(base_names)}"

    while department_name in existing_names:
        department_name = f"{random.choice(base_names)}"

    existing_names.add(department_name)

    return department_name


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными о департаментах и сотрудниках'

    def handle(self, *args, **kwargs):
        try:
            Department.objects.all().delete()
            Employee.objects.all().delete()

            total_employees = 60000
            num_departments = 30
            root_departments_count = 5
            employees_assigned = 0

            self.stdout.write(self.style.WARNING("Начинаем заполнение базы данных..."))

            departments = []
            existing_names = set()

            department_count = 0
            for dept_id in range(1, root_departments_count + 1):

                department_name = generate_department_name(existing_names)

                root_department = Department.objects.create(name=department_name, parent=None)
                departments.append(root_department)
                department_count += 1

                parent = root_department
                level = 2
                max_levels = 5

                while level <= max_levels and department_count < num_departments:
                    department_name = f"{parent.name.split(' - ')[0]} - Уровень {level}"
                    department = Department.objects.create(name=department_name, parent=parent)
                    departments.append(department)
                    parent = department
                    department_count += 1
                    level += 1

                    if department_count >= num_departments:
                        break

            employees_per_department = total_employees // len(departments)
            for department in departments:

                num_dept_employees = random.randint(employees_per_department - 1000, employees_per_department + 1000)

                for _ in range(num_dept_employees):
                    Employee.objects.create(
                        full_name=fake.name(),
                        position=fake.job(),
                        hire_date=fake.date_this_decade(),
                        salary=random.randint(30000, 120000),
                        department=department
                    )
                    employees_assigned += 1

            self.stdout.write(self.style.SUCCESS(
                f"База данных успешно заполнена. Создано {employees_assigned} сотрудников и "
                f"{len(departments)} отделов."))

        except Exception as e:
            error_message = f"Произошла ошибка при генерации данных: {e}"
            self.stdout.write(self.style.ERROR(error_message))
            logger.error(error_message)
            raise
