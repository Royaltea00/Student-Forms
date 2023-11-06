from django.shortcuts import render, redirect

from main_app.app_forms import StudentForm


# Create your views here.
def students(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    form = StudentForm()

    return render(request, 'students.html', {"form": form})