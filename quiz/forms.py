from django import forms
from .models import Quiz, QuizClass

class EditQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'description', 'public')
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control my_form"}),
            'description': forms.TextInput(attrs={'class':"form-control my_form"}),
            'public': forms.CheckboxInput(attrs={"class":"my_checkbox"}),
        }
        labels = {
            "name": "Nazwa",
            "description": "Opis",
            "public": "Czy quiz ma być publiczny?",
        }

class QuizClassForm(forms.ModelForm):
    class Meta:
        model = QuizClass
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control my_form"}),
        }
        labels = {
            "name": "Nazwa",
        }
