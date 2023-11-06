from django import forms

from main_app.models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields ="__all__"
