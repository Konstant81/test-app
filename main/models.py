from django.db import models

# Create your models here.
class Client(models.Model):
    fullname = models.CharField(max_length=100, null=False, verbose_name="имя_фамилия")

    class Meta:
        db_table = "client" # Имя таблицы в БД
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"

    def __str__(self):
        return str(self.fullname)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Заказчик')
    order_date = models.DateField(verbose_name="дата заказа")
    amount = models.IntegerField(null=False, verbose_name="сумма заказа")

    class Meta:
        db_table = "order"  # Имя таблицы в БД
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        # выполнение по умолчанию сортировки по убыванию даты заказов
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['-order_date']),
        ]

    def __str__(self):
        return str(self.id)
    