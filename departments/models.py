from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Название подразделения')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children',
                            verbose_name='Родительское подразделение')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    hire_date = models.DateField(verbose_name='Дата приема на работу')
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                 verbose_name='Размер заработной платы')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='employees',
                                   verbose_name='Подразделение')

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
