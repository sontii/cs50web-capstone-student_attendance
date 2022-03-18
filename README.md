# CS50's Web programming final project:
# Student attendance web application
#### Video Demo:  https://youtu.be/JAumF4IPF3o
------
## Description:


Student attendace support for school teachers and student keep track their classes, check notes, and communicate each other. Teacher can start courses, set the course capacity, and can assign teacher.  
Anonym users can explorer classes, regiustered users, can enroll selected courses, and download notes from courses. Students can send message their teachers.
Teacher can check enrolled student in each course, upload notes to course, rate every student, post news.

Written in django, javascript and json api.

------

### **How to use:**


Without registration you can browse all the courses, and news page.
You can register at registration page, with email password and your name. 

With student registration you can enroll courses, check your enrolled course on my
my course link. On the encolled course page, you can download notes. Can send 
message to your teachers. Every login toast message appear if you have unread message.

With teacher status can post news, on the news page, start new course in courses pages.
My course link will end you to your courses where you are the teacher.
Can list every course students, and check their profile.
Every login toast message appear if you have unread message.

in the top left the "Attendance" link will lend you to the main (news) page

"Log out" link will log out the system .

------

#### **Requirements:**



- django 3.2.4
- Python 3
- HTML5
- Bootstrap
- sqlite3
- javascript
- jquery

------

### **Launch:**


To run enter to the command line:

```
$ python manage.py runserver
```

------

### **Files and folders:**


- /capstone - main app
- /finalproject
- /db.sqlite3
- manage.py
- Readme.md - you are here
- reqirement.txt
#
- /capstone/media - stored course notes
- /capstone/static - css and javascript files
- /capstone/templates - html files
- /capstone/admin.py - administrator site config
- /capstone/models.py - database structure
- /capstone/urls.py - url structure 
- /capstone/view.py - view configuration file

------

### **Database:**

- Default user model was supplemented by student or teacher status field.
- Post table for storing news, with auto store date field.
- Course table used for storing Classes
- Messga table for teacher <-> student message
- Enrollment table for storing enroll information for classes,

the unique together means, student can enroll only one classes at one time.
teacher also enrolled to the course when teacher create new class

------

### **Views:**

- index page availbla all users without registration, this page show news.
- listCourse page show enrolled classes
- listStudent for listing student in selected class and able to set grades each student
- jsongrade is an api for update student grades with PUT and GET method
- students view for list selected courses enrolled students
- notes this view handle the file upload for course notes, teacher can upload or delete file, studnets only view restriction.
- messageList view listing messages when user logged in. This view also handle the post method when sending message someone.
- message this view show selected message content, where user can reply the message
- courses view show classes ordered by date. This view handle when teacher create new class
- mycourses handle the same as courses but filtered by logged user enrolled classes.
- json_all_enrollment API for all enrollment for json output
- jsonenrollment API for selected class enroll for json output
- jsoncourse API for seleted class for json output
- single_course view show selected course content.
- post view show content of the selected news item
- profile view show selected student profile page
- login view handle login requests
- logout view logout reuqest user
- register view for registering methods users

