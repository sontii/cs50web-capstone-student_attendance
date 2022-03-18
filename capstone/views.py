from re import T
from urllib.request import Request
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.core.files.storage import FileSystemStorage, default_storage
import datetime
import json
from .models import *

 # Create your views here.     

def index(request):
    post = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_counter = "a" * paginator.num_pages
    if request.user.is_authenticated:
        messageCounter = Message.objects.filter(receiver = request.user, read = False).count()
    else:
        messageCounter = None
    if request.method == "POST":
        postnew = request.POST["postnew"]
        title = request.POST["posttitle"]
        lpost = Post(user = request.user, post = postnew, title = title)
        lpost.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:
            
        return render(request, "index.html", {
            'page_obj': page_obj,
            'page_counter': page_counter,
            'messageCounter': messageCounter,
        })

@login_required(login_url='/login')
def listCourse(request):
    
    teacherCourses= Enrollment.objects.filter(student=request.user)
    return render(request, "listCourse.html", {
        'teacherCourses':teacherCourses,
    })

@login_required(login_url='/login')
def listStudent(request, courseid):
    studentList = Enrollment.objects.filter(course = courseid)
    return render(request, "listStudent.html", {
        'studentList':studentList,
    })

def jsongrade(request, enrollmentid): 
    if request.method == 'PUT':
        data = json.loads(request.body)
        enrollment_id = data.get('enrollment_id', '')
        grade = data.get('grade', '')
        try:
            grade = int(grade)
        except:
            grade = None
        if grade == None:
            return JsonResponse({
                        "error": "Error: only numbers between 1 and 100"}, status=300)
        else:
            if 0 <= grade <= 100:    
                updateGrade = Enrollment.objects.filter(id = enrollment_id)
                updateGrade.update(grade=grade)
                return JsonResponse({
                            "message": "Grade saved"}, status=201)
            else:
                return JsonResponse({
                            "error": "Error: only numbers between 1 and 100"}, status=300)
    else:
        get_enroll = Enrollment.objects.filter(pk=enrollmentid)
        get_enroll = list(get_enroll.values())
        return HttpResponse(json.dumps(get_enroll, indent=4, sort_keys=True, default=str))

@login_required(login_url='/login')
def students(request, courseid):
    student_list = Enrollment.objects.filter(course_id = courseid, student__is_teacher=False)
    return render(request, "studentlist.html", {
        'student_list': student_list,
    })

@login_required(login_url='/login')
def notes(request, courseid):
    pathupload = 'capstone/media/%i/' % (courseid)
    pathdir = '%i' % (courseid)
    
    #if delete file
    if request.method == 'POST' and 'deleteFile' in request.POST:
        deleteF = request.POST['deleteFile']
        fs = FileSystemStorage(location = pathupload)
        filename = fs.delete(deleteF)

        return HttpResponseRedirect(reverse("notes", kwargs={'courseid':courseid}))
    
    elif request.method == 'POST' and 'fileupload' in request.FILES:
        fileupload = request.FILES["fileupload"]
        fs = FileSystemStorage(location = pathupload)
        filename = fs.save(fileupload.name, fileupload)

        return HttpResponseRedirect(reverse("notes", kwargs={'courseid':courseid}))

    else:
        selected_course = Course.objects.get(id=courseid)
        try:
            filelist = FileSystemStorage().listdir(path=pathdir)
        except:
            filelist = None

        return render(request, "notes.html", {
            "selected_course": selected_course,
            "filelist": filelist,
        })

@login_required(login_url='/login')
def messagesList(request):
    messagesList = Message.objects.filter(receiver=request.user).order_by('-id')
    paginator = Paginator(messagesList, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_counter = "a" * paginator.num_pages
    course = list(Enrollment.objects.filter(student = request.user).values_list('course_id', flat=True))
    teacherList = list(Enrollment.objects.filter(course_id__in = course).values_list('student', flat=True))
    teacherList = User.objects.filter(id__in = teacherList, is_teacher=True)
    if request.method == "POST":
        receiver = request.POST["receiver"]
        receiver = User.objects.get(username = receiver)
        subject = request.POST["subject"]
        body = request.POST["body"]
        newMessage = Message(sender = request.user, receiver = receiver, subject = subject, body = body)
        newMessage.save()
        return HttpResponseRedirect(reverse("messagesList"))
    
    else:
            
        return render(request, "messages.html", {
            'messagesList': messagesList,
            'page_obj': page_obj,
            "page_counter": page_counter,
            'teacherList': teacherList,
        })

@login_required(login_url='/login')
def message(request, messageid):
    if request.method == "POST":
        receiver = request.POST["receiver"]
        receiver = User.objects.get(username = receiver)
        
        subject = request.POST["subject"]
        body = request.POST["body"]
        newMessage = Message(sender = request.user, receiver = receiver, subject = subject, body = body)
        newMessage.save()
        messages.success(request, 'Message sent')
        return HttpResponseRedirect(reverse("message", kwargs={'messageid': messageid}))
    
    else:
        singleMessage = Message.objects.get(pk=messageid)
        messageRead = Message.objects.filter(pk=messageid).values_list('read', flat=True)
        
        if False in messageRead:
            messageRead.update(read=True)

        return render(request, "message.html", {
            'message':singleMessage,
        })


def courses(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startdate = request.POST["startdate"]
        selectedteacher = request.POST["selectedteacher"]
        studentcap = request.POST["capacity"]
        teacher = User.objects.get(username=selectedteacher)
        newcourse = Course(title = title, description = description, started = startdate,
         capacity = studentcap)
        newcourse.save()
        newcourse.creator.add(request.user)
        newcourse.save()
        newenrollment = Enrollment(student = teacher, course = newcourse)
        newenrollment.save()
        return HttpResponseRedirect(reverse("courses"))

    else:
        nocourse = None
        courselist = Course.objects.all().order_by('-id')
        if not courselist:
            nocourse = True
        paginator = Paginator(courselist, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_counter = "a" * paginator.num_pages
        teacherlist = None
        current_date = datetime.date.today()
        if request.user.is_authenticated:
            teacherlist = User.objects.filter(is_teacher=1)
        
        return render(request, "courses.html", {
            'current_date':current_date,
            'teacherlist':teacherlist,
            'page_obj': page_obj,
            'nocourse': nocourse,
            'page_counter': page_counter,
        })

def mycourses(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startdate = request.POST["startdate"]
        selectedteacher = request.POST["selectedteacher"]
        studentcap = request.POST["capacity"]
        teacher = User.objects.get(username=selectedteacher)
        newcourse = Course(title = title, description = description, started = startdate,
         capacity = studentcap)
        newcourse.save()
        newcourse.teacher.add(teacher)
        newcourse.creator.add(request.user)
        newcourse.save()
        return HttpResponseRedirect(reverse("mycourses"))

    else:
        nocourse = None
        enrollList = Enrollment.objects.filter(student_id = request.user.id).values_list('course', flat=True)
        courselist = Course.objects.filter(pk__in = enrollList).order_by('-id')
        if not courselist:
            nocourse = True
        paginator = Paginator(courselist, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_counter = "a" * paginator.num_pages
        current_date = datetime.date.today()
        return render(request, "mycourses.html", {
            'current_date':current_date,
            'page_obj': page_obj,
            'nocourse': nocourse,
            'page_counter': page_counter,
        })


def json_all_enrollment(request): 
    if request.method == 'PUT':
        data = json.loads(request.body)
        course_id = data.get('course_id', '')
        add_user = Enrollment(course_id = course_id, student_id = request.user.id)
        add_user.save()
        return JsonResponse({
                    "message": "saved"}, status=201)
    else:
        get_enroll = Enrollment.objects.all()
        get_enroll = list(get_enroll.values())
        return HttpResponse(json.dumps(get_enroll, indent=4, default=str))


def jsonenrollment(request, enrollmentid): 
    if request.method == 'PUT':
        data = json.loads(request.body)
        course_id = data.get('course_id', '')
        student_id = data.get('student_id', '')
        add_user = Enrollment(course_id = course_id, student_id = student_id)
        add_user.save()
        return JsonResponse({
                    "message": "saved"}, status=201)
    else:
        get_enroll = Enrollment.objects.filter(pk=enrollmentid)
        get_enroll = list(get_enroll.values())
        return HttpResponse(json.dumps(get_enroll, indent=4, sort_keys=True, default=str))

def jsoncourse(request, courseid):
    single_course = Course.objects.filter(id = courseid)
    single_course = list(single_course.values())
    return HttpResponse(json.dumps(single_course, indent=4, sort_keys=True, default=str))


def single_course(request, courseid):
    single_course = Course.objects.get(id = courseid)
    enrolled = None
    get_enroll_id = None
    try:
        get_enroll_id = Enrollment.objects.get(course_id = courseid, student_id = request.user.id)
        enrolled = True
    except:
        enrolled = False
    
    capacity_counter = Enrollment.objects.filter(course_id = courseid, student__is_teacher=False).count()
    max_capacity = single_course.capacity
    space_left = max_capacity - capacity_counter
    courseTeacher = list(Enrollment.objects.filter(course_id = courseid).values_list('course_id', flat=True))
    courseTeacher = list(Enrollment.objects.filter(course_id__in = courseTeacher).values_list('student', flat=True))
    courseTeacher = User.objects.filter(id__in = courseTeacher, is_teacher=True)

    return render(request, "course.html", {
        'course':single_course,
        'enrollment':get_enroll_id,
        'enrolled':enrolled,
        'space_left':space_left,
        'courseTeacher':courseTeacher,
    })


def post(request, postid):
    post = Post.objects.filter(id = postid)
    if not post:
        return render(request, "404.html", {
        'post': postid,
    })
    else:
        return render(request, "post.html", {
            'post': post,
        })

@login_required(login_url='/login')
def profile(request):
    userprofile = User.objects.filter(id = request.user.id)
    return render(request, "profile.html", {
        'userprofile': userprofile,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name = firstname, last_name = lastname)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")