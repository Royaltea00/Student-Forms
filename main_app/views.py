from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

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
    data = Student.objects.all()     # SELECT * FROM students
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

    return render(request,'display.html', {"students": data})
# show?page=1


def show_details(request, student_id):
    student = Student.objects.get(pk=student_id) # SELECT * FROM students WHERE id=1
    return render(request, 'details.html', {'student': student})


def delete_student(request, student_id):
    # get student from db
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect("show")


def students_search(request):
    search = request.GET["search"]
    data = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))

    if search.isnumeric():
        score = int(search)
        data = Student.objects.filter(kcpe_score=score)

    paginator = Paginator(data, 50)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request,'display.html', {"students": data})