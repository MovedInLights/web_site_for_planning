from django.forms import ModelForm  # Импортируем форму
from .models import Todo  # Импортируем модель из файла моделс


# Создаем модель с классом Мета и всеми полями,
# которые будут нужны пользователю для создания задачи
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']
