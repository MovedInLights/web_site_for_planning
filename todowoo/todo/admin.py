from django.contrib import admin
from .models import Todo


# Наследуем класс из ModelAdmin
class TodoAmin(admin.ModelAdmin):
    # Обязательно запятая после названия поля
    readonly_fields = ('created',)


# Добавляем сюда класс в качестве аргумента
admin.site.register(Todo, TodoAmin)
