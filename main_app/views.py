from django.shortcuts import render, redirect

from main_app.app_forms import StudentForm
from main_app.models import Student


# Create your views here.
def students(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = StudentForm()

    return render(request, 'students.html', {"form": form})


def show_students(request):
    data = Student.objects.all()     # SELECT = FROM students
    return render(request,'display.html', {"students": data})


def show_details(request, id):
    student = Student.objects.get(pk=id) # SELECT * FROM students WHERE id=1
    return render(request, 'details.html', {'student': student})