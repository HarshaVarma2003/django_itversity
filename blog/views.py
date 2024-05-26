# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Post, Subject, StudyMaterial, PreviousYearQuestion, Announcement, Reminder
from .forms import ReminderForm

def home(request):
    # Query for subjects
    query = request.GET.get('q')
    if query:
        subjects = Subject.objects.filter(name__icontains=query)
    else:
        subjects = Subject.objects.all()

    # Query for announcements
    announcements = Announcement.objects.all()

    # Handle reminder form submission
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = ReminderForm()

    # Query for reminders
    reminders = Reminder.objects.all()

    return render(request, 'blog/home.html', {
        'subjects': subjects,
        'announcements': announcements,
        'form': form,
        'reminders': reminders
    })

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def help(request):
    return render(request, 'blog/help.html', {'title': 'Help'})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    study_materials = subject.study_materials.all()
    previous_questions = subject.previousyearquestion_set.all()
    return render(request, 'blog/subject_detail.html', {
        'subject': subject,
        'study_materials': study_materials,
        'previous_questions': previous_questions
    })

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-home')
        else:
            return HttpResponse('Invalid login credentials')
    else:
        return render(request, 'blog/login.html')
