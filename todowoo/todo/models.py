from django.db import models
from django.contrib.auth.models import User  # импортиреуем пользователя


class Todo(models.Model):
    title = models.CharField(max_length=100)
    # Иногда пользователь будет создавать запись без описания
    memo = models.TextField(blank=True)
    # Значение создается автоматически
    created = models.DateTimeField(null=True, auto_now_add=True)
    # Для поля "дата" мы используем "Null"
    datecompleted = models.DateTimeField(null=True, blank=True)
    # Флаг важности и значение по умолчанию "не стоит"
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
