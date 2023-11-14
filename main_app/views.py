from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import StudentForm, LoginForm
from main_app.models import Student


# Create your views here.
def students(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student saved successfully")
            # messages.error(request, 'Error while saving Student')
            # messages.warning(request, "This action is irreversible")
            # messages.info(request, "Tomorrow might be a holiday. Check your calendar")
            return redirect("home")
    else:
        form = StudentForm()

    return render(request, 'students.html', {"form": form})


def show_students(request):
    data = Student.objects.all()  # SELECT * FROM students
    # data = Student.objects.all().order_by('-kcpe_score') # lists students acc to kcpe in descending order
    # data= Student.objects.filter(first_name='Gran') # case-sensitive
    # data= Student.objects.filter(first_name__startswith='Rob') # case-insensitive
    # data= Student.objects.filter(first_name__icontains='Rob')
    # data= Student.objects.filter(first_name__icontains='Rob', last_name__icontains='sh') # AND
    # data= Student.objects.filter(first_name__icontains='Rob') | Student.objects.filter(last_name__icontains='ht') # OR
    # data = Student.objects.filter(dob__year= 2000, dob__month=12) #only those born in Dec 2000

    # today= datetime.today()
    # mon = today.month
    # day = today.day
    # data =Student.objects.filter(dob__month=mon, dob__day=day)
    paginator = Paginator(data, 50)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)

    return render(request, 'display.html', {"students": data})


# show?page=1


def show_details(request, id):
    student = Student.objects.get(pk=id)  # SELECT * FROM students WHERE id=1
    return render(request, 'details.html', {'student': student})


def delete_student(request, student_id):
    # get student from db
    student = get_object_or_404(Student, pk=student_id)  # SELECT * FROM students WHERE id=1
    student.delete()
    messages.info(request, f"Student {student.first_name}{student.last_name} was deleted successfully")
    return redirect("show")


def students_search(request):
    search = request.GET["search"]
    data = Student.objects.filter(
        Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))

    if search.isnumeric():
        score = int(search)
        data = Student.objects.filter(kcpe_score=score)

    paginator = Paginator(data, 50)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, 'display.html', {"students": data})


def update_student(request, student_id):
    # get student from db
    student = get_object_or_404(Student, pk=student_id)  # SELECT * FROM students WHERE id=1
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated student {student.first_name}")
            return redirect("details", student_id)
    else:
        form = StudentForm(instance=student)
    return render(request, "update.html", {"form": form})


def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Signed in successfully')
                return redirect('home')
        messages.error(request, "Invalid username or password")
        return render(request, 'login.html', {"form": form})



def signout(request):
    return None
