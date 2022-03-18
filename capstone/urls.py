from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("courses", views.courses, name="courses"),
    path("listCourse", views.listCourse, name="listCourse"),
    path("listStudent/<int:courseid>", views.listStudent, name="listStudent"),
    path("mycourses", views.mycourses, name="mycourses"),
    path("messages", views.messagesList, name="messagesList"),
    path("message/<int:messageid>", views.message, name="message"),
    path("notes/<int:courseid>", views.notes, name="notes"),
    path("course/<int:courseid>", views.single_course, name="single_course"),
    path("post/<int:postid>", views.post, name="post"),
    path("students/<int:courseid>", views.students, name="students"),
    path("api/course/<int:courseid>", views.jsoncourse, name="jsoncourse"),
    path("api/enrollment", views.json_all_enrollment, name="json_all_enrollment"),
    path("api/enrollment/<int:enrollmentid>", views.jsonenrollment, name="jsonenrollment"),
    path("api/grades/<int:enrollmentid>", views.jsongrade, name="jsongrade"),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)